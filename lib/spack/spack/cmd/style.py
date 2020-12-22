# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import re
import os
import sys
import argparse

if sys.version_info < (3, 0):
    from itertools import izip_longest  # novm

    zip_longest = izip_longest
else:
    from itertools import zip_longest  # novm

from llnl.util.filesystem import working_dir

import spack.paths
from spack.util.executable import which


description = (
    "runs source code style checks on Spack. requires flake8, mypy, black for"
    + "their respective checks"
)
section = "developer"
level = "long"


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


#: List of directories to exclude from checks.
exclude_directories = [spack.paths.external_path]

#: max line length we're enforcing (note: this duplicates what's in .flake8)
max_line_length = 79


def changed_files(base=None, untracked=True, all_files=False):
    """Get list of changed files in the Spack repository."""

    git = which("git", required=True)

    if base is None:
        base = os.environ.get("TRAVIS_BRANCH", "develop")

    range = "{0}...".format(base)

    git_args = [
        # Add changed files committed since branching off of develop
        ["diff", "--name-only", "--diff-filter=ACMR", range],
        # Add changed files that have been staged but not yet committed
        ["diff", "--name-only", "--diff-filter=ACMR", "--cached"],
        # Add changed files that are unstaged
        ["diff", "--name-only", "--diff-filter=ACMR"],
    ]

    # Add new files that are untracked
    if untracked:
        git_args.append(["ls-files", "--exclude-standard", "--other"])

    # add everything if the user asked for it
    if all_files:
        git_args.append(["ls-files", "--exclude-standard"])

    excludes = [os.path.realpath(f) for f in exclude_directories]
    changed = set()

    for arg_list in git_args:
        files = git(*arg_list, output=str).split("\n")

        for f in files:
            # Ignore non-Python files
            if not (f.endswith(".py") or f == "bin/spack"):
                continue

            # Ignore files in the exclude locations
            if any(os.path.realpath(f).startswith(e) for e in excludes):
                continue

            changed.add(f)

    return sorted(changed)


def setup_parser(subparser):
    subparser.add_argument(
        "-b",
        "--base",
        action="store",
        default=None,
        help="select base branch for collecting list of modified files",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="check all files, not just changed files",
    )
    subparser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="send filtered files to stdout as well as temp files",
    )
    subparser.add_argument(
        "-r",
        "--root-relative",
        action="store_true",
        default=False,
        help="print root-relative paths (default: cwd-relative)",
    )
    subparser.add_argument(
        "-U",
        "--no-untracked",
        dest="untracked",
        action="store_false",
        default=True,
        help="exclude untracked files from checks",
    )
    subparser.add_argument(
        "--no-flake8",
        dest="flake8",
        action="store_false",
        help="Do not run flake8, default is run flake8",
    )
    subparser.add_argument(
        "--no-mypy",
        dest="mypy",
        action="store_false",
        help="Do not run mypy, default is run mypy if available",
    )
    subparser.add_argument(
        "files", nargs=argparse.REMAINDER, help="specific files to check"
    )


def rewrite_and_print_output(output, args):
    """rewrite ouput with <file>:<line>: format to respect path args"""
    if args.root_relative:
        # print results relative to repo root.
        print(output)
    else:
        # print results relative to current working directory
        def cwd_relative(path):
            return "{0}: [".format(
                os.path.relpath(
                    os.path.join(spack.paths.prefix, path.group(1)),
                    os.getcwd(),
                )
            )

        for line in output.split("\n"):
            print(re.sub(r"^(.*): \[", cwd_relative, line))


def print_style_header(file_list, args):
    print("=======================================================")
    print("style: running code checks on spack.")
    print("tools:")
    if args.flake8:
        print("  flake8")
    if args.mypy:
        print("  mypy")
    print()
    print("Modified files:")
    for filename in file_list:
        print("  {0}".format(filename.strip()))
    print("=======================================================")


def print_tool_header(tool):
    print("=======================================================")
    print("style: running %s checks on spack." % tool)
    print("=======================================================")


def run_flake8(file_list, args):
    returncode = 0
    print_tool_header("flake8")
    flake8_cmd = which("flake8", required=True)

    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        chunk = filter(lambda e: e is not None, chunk)

        output = flake8_cmd(
            # use .flake8 implicitly to work around bug in flake8 upstream
            # append-config is ignored if `--config` is explicitly listed
            # see: https://gitlab.com/pycqa/flake8/-/issues/455
            # "--config=.flake8",
            *chunk,
            fail_on_error=False,
            output=str
        )
        returncode |= flake8_cmd.returncode

        rewrite_and_print_output(output, args)

    if returncode == 0:
        print("Flake8 style checks were clean")
    return returncode


def run_mypy(file_list, args):
    mypy_cmd = which("mypy")
    if mypy_cmd is None:
        print("style: mypy is not available in path, skipping")
        return 1

    print_tool_header("mypy")

    returncode = 0
    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        chunk = filter(lambda e: e is not None, chunk)

        output = mypy_cmd(*chunk, fail_on_error=False, output=str)
        returncode |= mypy_cmd.returncode

        rewrite_and_print_output(output, args)

    if returncode == 0:
        print("mypy style checks were clean")
    return returncode


def style(parser, args):
    file_list = args.files
    if file_list:

        def prefix_relative(path):
            return os.path.relpath(
                os.path.abspath(os.path.realpath(path)), spack.paths.prefix
            )

        file_list = [prefix_relative(p) for p in file_list]

    returncode = 0
    with working_dir(spack.paths.prefix):
        if not file_list:
            file_list = changed_files(args.base, args.untracked, args.all)
        print_style_header(file_list, args)
        if args.flake8:
            returncode = run_flake8(file_list, args)
        if args.mypy:
            returncode |= run_mypy(file_list, args)

    if returncode != 0:
        print("spack style found errors.")
        sys.exit(1)
    else:
        print("spack style checks were clean.")
