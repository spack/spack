#!/usr/bin/env python3
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Check that direct uses of ``os.symlink`` in Spack do not increase.

``os.symlink`` fails on Windows unless the user has symlink privileges. Spack should use
``spack.util.filesystem.symlink`` instead, which falls back to junctions and hard links."""

import argparse
import ast
import os
import sys
from typing import Dict, List, Sequence


def symlink_usages(tree: ast.AST) -> List[int]:
    """Return the line numbers of references to ``os.symlink`` (calls or aliases),
    ``from os import symlink`` and ``Path.symlink_to``, which are all ``os.symlink``."""
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            is_os_symlink = (
                node.attr == "symlink"
                and isinstance(node.value, ast.Name)
                and node.value.id == "os"
            )
            if is_os_symlink or node.attr == "symlink_to":
                lines.append(node.lineno)
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            lines.extend(node.lineno for alias in node.names if alias.name == "symlink")
    return sorted(lines)


def collect(root: str, exclude: Sequence[str]) -> Dict[str, List[int]]:
    """Map each Python file under root, relative to root, to its ``os.symlink`` usages."""
    usages = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded top-level directories instead of walking them
        if dirpath == root:
            dirnames[:] = [d for d in dirnames if d not in exclude]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, "rb") as f:
                contents = f.read()
            # Every pattern we look for contains "symlink", so only parse files that mention it
            if b"symlink" not in contents:
                continue
            lines = symlink_usages(ast.parse(contents, filename=path))
            if lines:
                usages[os.path.relpath(path, root).replace(os.sep, "/")] = lines
    return usages


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", required=True, help="module root of the commit to compare against"
    )
    parser.add_argument("root", help="module root of the commit to check")
    parser.add_argument(
        "--exclude",
        action="append",
        default=["test", "vendor"],
        help="top-level directory under the module root to skip (default: test, vendor)",
    )
    args = parser.parse_args(argv)

    old = collect(args.baseline, args.exclude)
    new = collect(args.root, args.exclude)
    old_total = sum(len(lines) for lines in old.values())
    new_total = sum(len(lines) for lines in new.values())

    # Report per file, but only fail on the global count, so moving a usage is not an error
    print(f"os.symlink usages: {old_total} -> {new_total}")
    for rel_path in sorted(old.keys() | new.keys()):
        old_count = len(old.get(rel_path, []))
        new_lines = new.get(rel_path, [])
        marker = "+" if len(new_lines) > old_count else "-" if len(new_lines) < old_count else " "
        where = ", ".join(f"{rel_path}:{line}" for line in new_lines)
        print(
            f"{marker} {rel_path}: {old_count} -> {len(new_lines)}"
            + (f" ({where})" if where else "")
        )

    if new_total > old_total:
        sys.stdout.flush()
        print(
            "error: direct use of os.symlink increased. Use spack.util.filesystem.symlink, "
            "which works on Windows without symlink privileges.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
