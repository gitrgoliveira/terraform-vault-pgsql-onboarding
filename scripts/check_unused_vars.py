#!/usr/bin/env python3
"""Pre-commit gate: fail on input variables that do no real work.

Terraform's own tooling and tflint's `terraform_unused_declarations` do NOT catch
a variable that is referenced only inside an `output` block as a bare pass-through
(`value = var.x`), because that reference counts as "used". This check closes that
gap.

For every directory that contains `.tf` files (each is a Terraform module), every
declared input variable is classified by where it is actually referenced:

  real use          - referenced in any non-`variable`/non-`output` block
                      (resource, data, module, locals, provider, ...)  -> OK
  computed output   - referenced inside an `output` that transforms it, e.g.
                      templatefile(), interpolation, functions                -> OK
  pure echo         - referenced ONLY as a bare `value = var.x` in an output   -> FAIL
  validation only   - referenced ONLY in another variable's validation block   -> FAIL
  unused            - not referenced anywhere                                   -> FAIL

A variable may be exempted by placing an allow marker inside its `variable` block:

    variable "vault_address" {
      type        = string
      description = "..."
      # echo-scan:allow render-only value echoed for the IDP/downstream handoff
    }

Exit code is non-zero when any non-exempt violation is found.
"""
from __future__ import annotations

import os
import re
import sys

BLOCK_HEADER = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*(?:"[^"]*"\s*)*\{')
VAR_DECL = re.compile(r'variable\s+"([^"]+)"')
ALLOW_MARKER = re.compile(r'#\s*echo-scan:allow\b[ \t]*(.*)')
SKIP_DIRS = {'.git', '.terraform', 'node_modules'}

FAIL_KINDS = {'PURE-ECHO', 'VALIDATION-ONLY', 'UNUSED'}
REMEDIATION = {
    'PURE-ECHO': 'referenced only as a bare `value = var.NAME` in an output',
    'VALIDATION-ONLY': "referenced only in another variable's validation block",
    'UNUSED': 'not referenced anywhere in the module',
}


def mask(text: str) -> str:
    """Blank out comments, double-quoted strings, and heredocs (newlines kept) so
    brace/quote handling is reliable for block segmentation. Never used for
    reference detection."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == '//' or c == '#':
            j = text.find('\n', i)
            j = n if j == -1 else j
            out.append(' ' * (j - i))
            i = j
            continue
        if two == '/*':
            j = text.find('*/', i + 2)
            j = n if j == -1 else j + 2
            out.append(''.join(ch if ch == '\n' else ' ' for ch in text[i:j]))
            i = j
            continue
        if two == '<<':
            m = re.match(r'<<-?["\']?([A-Za-z_][A-Za-z0-9_]*)["\']?\r?\n', text[i:])
            if m:
                tag = m.group(1)
                end = re.search(r'\n[ \t]*' + re.escape(tag) + r'\b', text[i:])
                j = n if not end else i + end.end()
                out.append(''.join(ch if ch == '\n' else ' ' for ch in text[i:j]))
                i = j
                continue
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            j = min(j + 1, n)
            out.append(''.join(ch if ch == '\n' else ' ' for ch in text[i:j]))
            i = j
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def blocks(text: str):
    """Yield (block_type, header_label, body_original_text) for top-level blocks."""
    masked = mask(text)
    for m in BLOCK_HEADER.finditer(masked):
        btype = m.group(1)
        if btype in ('for', 'if', 'in'):
            continue
        open_brace = m.end() - 1
        depth, j = 0, m.end() - 1
        while j < len(masked):
            ch = masked[j]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[open_brace + 1:j]
        label_m = re.search(r'"([^"]*)"', text[m.start():open_brace])
        yield btype, (label_m.group(1) if label_m else ''), body


def scan_dir(d: str, tf_files: list[str]):
    declared: dict[str, str] = {}
    allow: dict[str, str] = {}
    all_blocks = []
    for f in tf_files:
        with open(os.path.join(d, f), encoding='utf-8') as fh:
            text = fh.read()
        for name in VAR_DECL.findall(text):
            declared[name] = f
        for btype, label, body in blocks(text):
            all_blocks.append((f, btype, label, body))
            if btype == 'variable':
                mk = ALLOW_MARKER.search(body)
                if mk:
                    allow[label] = mk.group(1).strip()

    findings = []
    for var, decl_file in sorted(declared.items()):
        if var in allow:
            continue
        pat = re.compile(r'\bvar\.' + re.escape(var) + r'\b')
        bare = re.compile(r'value\s*=\s*var\.' + re.escape(var) + r'\s*(#.*)?$',
                          re.MULTILINE)
        real = pure_echo = computed_output = validation = False
        for _f, btype, label, body in all_blocks:
            if not pat.search(body):
                continue
            if btype == 'output':
                if bare.search(body) and len(pat.findall(body)) == 1:
                    pure_echo = True
                else:
                    computed_output = True
            elif btype == 'variable':
                if label != var:
                    validation = True
            else:
                real = True
        if real or computed_output:
            continue
        if pure_echo:
            findings.append((var, 'PURE-ECHO', decl_file))
        elif validation:
            findings.append((var, 'VALIDATION-ONLY', decl_file))
        else:
            findings.append((var, 'UNUSED', decl_file))
    return findings, allow


def main(argv: list[str]) -> int:
    roots = [a for a in argv[1:] if not a.startswith('-')] or ['.']
    module_dirs: dict[str, list[str]] = {}
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [x for x in dirnames if x not in SKIP_DIRS]
            tf = sorted(f for f in filenames if f.endswith('.tf'))
            if tf:
                module_dirs[dirpath] = tf

    violations = 0
    modules = 0
    allowed_total = 0
    for d in sorted(module_dirs):
        modules += 1
        findings, allow = scan_dir(d, module_dirs[d])
        allowed_total += len(allow)
        if findings:
            rel = os.path.relpath(d)
            print(f'  {rel}')
            for var, kind, f in findings:
                violations += 1
                print(f'    FAIL  {kind:15} var.{var}  ({f})')
                print(f'          {REMEDIATION[kind]}')

    if violations:
        print()
        print(f'echo-scan: {violations} violation(s) across {modules} module(s).')
        print('Fix by using the variable in module logic, removing it, or marking it')
        print('intentional with `# echo-scan:allow <reason>` inside the variable block.')
        return 1

    print(f'echo-scan: OK ({modules} module(s) scanned, '
          f'{allowed_total} allow-listed variable(s)).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
