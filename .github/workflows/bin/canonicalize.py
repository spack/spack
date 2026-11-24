#!/usr/bin/env python3
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import ast
import os
import subprocess
import sys
from itertools import product
from typing import List


def run_git_command(*args: str, dir: str) -> None:
    """Run a git command in the output directory."""
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=example@example.com",
            "-c",
            "user.name=Example",
            "-c",
            "init.defaultBranch=main",
            "-c",
            "color.ui=always",
            "-C",
            dir,
            *args,
        ],
        check=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


def run(root: str, output_dir: str) -> None:
    """Recurse over a directory and canonicalize all Python files."""
    from spack.util.package_hash import RemoveDocstrings, unparse

    count = 0
    stack = [root]

    while stack:
        current = stack.pop()
        for entry in os.scandir(current):
            if entry.is_dir(follow_symlinks=False):
                stack.append(entry.path)
            elif entry.is_file(follow_symlinks=False) and entry.name.endswith(".py"):
                try:
                    with open(entry.path, "r") as f:
                        src = f.read()
                except OSError:
                    continue

                canonical_dir = os.path.join(output_dir, os.path.relpath(current, root))
                os.makedirs(canonical_dir, exist_ok=True)
                with open(os.path.join(canonical_dir, entry.name), "w") as f:
                    f.write(
                        unparse(RemoveDocstrings().visit(ast.parse(src)), py_ver_consistent=True)
                    )
                count += 1

    assert count > 0, "No Python files found in the specified directory."


def compare(
    input_dir: str, output_dir: str, python_versions: List[str], spack_versions: List[str]
) -> None:
    """Compare canonicalized files across different Python versions and error if they differ."""
    # Create a git repo in output_dir to track changes
    os.makedirs(output_dir, exist_ok=True)
    run_git_command("init", dir=output_dir)

    pairs = list(product(spack_versions, python_versions))

    if len(pairs) < 2:
        raise ValueError("At least two Python or two Spack versions must be given for comparison.")

    changes_with_previous: List[int] = []

    for i, (spack_dir, python_exe) in enumerate(pairs):
        print(f"\033[1;97mCanonicalizing with {python_exe} and {spack_dir}...\033[0m", flush=True)

        # Point PYTHONPATH to the given Spack library for the subprocess
        if not os.path.isdir(spack_dir):
            raise ValueError(f"Invalid Spack dir: {spack_dir}")
        env = os.environ.copy()
        spack_pythonpath = os.path.join(spack_dir, "lib", "spack")
        if "PYTHONPATH" in env and env["PYTHONPATH"]:
            env["PYTHONPATH"] = f"{spack_pythonpath}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = spack_pythonpath

        subprocess.run(
            [python_exe, __file__, "--run", "--input-dir", input_dir, "--output-dir", output_dir],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=env,
        )
        if i > 0:
            try:
                run_git_command("diff", "--exit-code", "HEAD", dir=output_dir)
            except subprocess.CalledProcessError:
                changes_with_previous.append(i)

        # The first run creates a commit for reference
        run_git_command("add", ".", dir=output_dir)
        run_git_command(
            "commit",
            "--quiet",
            "--allow-empty",  # makes this idempotent when running locally
            "-m",
            f"Canonicalized with {python_exe} and {spack_dir}",
            dir=output_dir,
        )

    for i in changes_with_previous:
        previous_spack, previous_python = pairs[i - 1]
        current_spack, current_python = pairs[i]
        print(
            f"\033[1;31mChanges detected between {previous_python} ({previous_spack}) and "
            f"{current_python} ({current_spack})\033[0m"
        )

    if changes_with_previous:
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Canonicalize Spack package files.")
    parser.add_argument("--run", action="store_true", help="Generate canonicalized sources.")
    parser.add_argument("--spack", nargs="+", help="Specify one or more Spack versions.")
    parser.add_argument("--python", nargs="+", help="Specify one or more Python versions.")
    parser.add_argument("--input-dir", type=str, required=True, help="A repo's packages dir.")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="The output directory for canonicalized package files.",
    )
    args = parser.parse_args()

    if args.run:
        run(args.input_dir, args.output_dir)
    else:
        compare(args.input_dir, args.output_dir, args.python, args.spack)
