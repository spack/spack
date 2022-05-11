# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import os
import re
import sys

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.filesystem import working_dir

import spack.bootstrap
import spack.paths
from spack.util.executable import which

if sys.version_info < (3, 0):
    from itertools import izip_longest  # novm

    zip_longest = izip_longest
else:
    from itertools import zip_longest  # novm


description = "runs source code style checks on spack"
section = "developer"
level = "long"


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    for group in zip_longest(*args, fillvalue=fillvalue):
        yield filter(None, group)


#: List of directories to exclude from checks -- relative to spack root
exclude_directories = [
    os.path.relpath(spack.paths.external_path, spack.paths.prefix),
]

#: Order in which tools should be run. flake8 is last so that it can
#: double-check the results of other tools (if, e.g., --fix was provided)
#: The list maps an executable name to a spack spec needed to install it.
tool_order = [
    ("isort", spack.bootstrap.ensure_isort_in_path_or_raise),
    ("mypy", spack.bootstrap.ensure_mypy_in_path_or_raise),
    ("black", spack.bootstrap.ensure_black_in_path_or_raise),
    ("flake8", spack.bootstrap.ensure_flake8_in_path_or_raise),
]

#: tools we run in spack style
tools = {}


def is_package(f):
    """Whether flake8 should consider a file as a core file or a package.

    We run flake8 with different exceptions for the core and for
    packages, since we allow `from spack import *` and poking globals
    into packages.
    """
    return f.startswith("var/spack/repos/")


#: decorator for adding tools to the list
class tool(object):
    def __init__(self, name, required=False):
        self.name = name
        self.required = required

    def __call__(self, fun):
        tools[self.name] = (fun, self.required)
        return fun


def changed_files(base="develop", untracked=True, all_files=False, root=None):
    """Get list of changed files in the Spack repository.

    Arguments:
        base (str): name of base branch to evaluate differences with.
        untracked (bool): include untracked files in the list.
        all_files (bool): list all files in the repository.
        root (str): use this directory instead of the Spack prefix.
    """
    if root is None:
        root = spack.paths.prefix

    git = which("git", required=True)

    # ensure base is in the repo
    git("show-ref", "--verify", "--quiet", "refs/heads/%s" % base,
        fail_on_error=False)
    if git.returncode != 0:
        tty.die(
            "This repository does not have a '%s' branch." % base,
            "spack style needs this branch to determine which files changed.",
            "Ensure that '%s' exists, or specify files to check explicitly." % base
        )

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

    excludes = [
        os.path.realpath(os.path.join(root, f))
        for f in exclude_directories
    ]
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
        default="develop",
        help="branch to compare against to determine changed files (default: develop)",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="check all files, not just changed files",
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
        "-f",
        "--fix",
        action="store_true",
        default=False,
        help="format automatically if possible (e.g., with isort, black)",
    )
    subparser.add_argument(
        "--no-isort",
        dest="isort",
        action="store_false",
        help="do not run isort (default: run isort if available)",
    )
    subparser.add_argument(
        "--no-flake8",
        dest="flake8",
        action="store_false",
        help="do not run flake8 (default: run flake8 or fail)",
    )
    subparser.add_argument(
        "--no-mypy",
        dest="mypy",
        action="store_false",
        help="do not run mypy (default: run mypy if available)",
    )
    subparser.add_argument(
        "--black",
        dest="black",
        action="store_true",
        help="run black if available (default: skip black)",
    )
    subparser.add_argument(
        "--root",
        action="store",
        default=None,
        help="style check a different spack instance",
    )
    subparser.add_argument(
        "files", nargs=argparse.REMAINDER, help="specific files to check"
    )


def cwd_relative(path, args):
    """Translate prefix-relative path to current working directory-relative."""
    return os.path.relpath(os.path.join(args.root, path), args.initial_working_dir)


def rewrite_and_print_output(
    output, args, re_obj=re.compile(r"^(.+):([0-9]+):"), replacement=r"{0}:{1}:"
):
    """rewrite ouput with <file>:<line>: format to respect path args"""
    # print results relative to current working directory
    def translate(match):
        return replacement.format(
            cwd_relative(match.group(1), args), *list(match.groups()[1:])
        )

    for line in output.split("\n"):
        if not line:
            continue
        if not args.root_relative and re_obj:
            line = re_obj.sub(translate, line)
        print("  " + line)


def print_style_header(file_list, args):
    tools = [tool for tool, _ in tool_order if getattr(args, tool)]
    tty.msg("Running style checks on spack", "selected: " + ", ".join(tools))

    # translate modified paths to cwd_relative if needed
    paths = [filename.strip() for filename in file_list]
    if not args.root_relative:
        paths = [cwd_relative(filename, args) for filename in paths]

    tty.msg("Modified files", *paths)
    sys.stdout.flush()


def print_tool_header(tool):
    sys.stdout.flush()
    tty.msg("Running %s checks" % tool)
    sys.stdout.flush()


def print_tool_result(tool, returncode):
    if returncode == 0:
        color.cprint("  @g{%s checks were clean}" % tool)
    else:
        color.cprint("  @r{%s found errors}" % tool)


@tool("flake8", required=True)
def run_flake8(flake8_cmd, file_list, args):
    returncode = 0
    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        output = flake8_cmd(
            # always run with config from running spack prefix
            "--config=%s" % os.path.join(spack.paths.prefix, ".flake8"),
            *chunk,
            fail_on_error=False,
            output=str
        )
        returncode |= flake8_cmd.returncode

        rewrite_and_print_output(output, args)

    print_tool_result("flake8", returncode)
    return returncode


@tool("mypy")
def run_mypy(mypy_cmd, file_list, args):
    # always run with config from running spack prefix
    mypy_args = [
        "--config-file", os.path.join(spack.paths.prefix, "pyproject.toml"),
        "--package", "spack",
        "--package", "llnl",
        "--show-error-codes",
    ]
    # not yet, need other updates to enable this
    # if any([is_package(f) for f in file_list]):
    #     mypy_args.extend(["--package", "packages"])

    output = mypy_cmd(*mypy_args, fail_on_error=False, output=str)
    returncode = mypy_cmd.returncode

    rewrite_and_print_output(output, args)

    print_tool_result("mypy", returncode)
    return returncode


@tool("isort")
def run_isort(isort_cmd, file_list, args):
    # always run with config from running spack prefix
    isort_args = ("--settings-path", os.path.join(spack.paths.prefix, "pyproject.toml"))
    if not args.fix:
        isort_args += ("--check", "--diff")

    pat = re.compile("ERROR: (.*) Imports are incorrectly sorted")
    replacement = "ERROR: {0} Imports are incorrectly sorted"
    returncode = [0]

    def process_files(file_list, is_args):
        for chunk in grouper(file_list, 100):
            packed_args = is_args + tuple(chunk)
            output = isort_cmd(*packed_args, fail_on_error=False, output=str, error=str)
            returncode[0] |= isort_cmd.returncode

            rewrite_and_print_output(output, args, pat, replacement)

    packages_isort_args = ('--rm', 'spack', '--rm', 'spack.pkgkit', '--rm',
                           'spack.package_defs', '-a', 'from spack.package import *')
    packages_isort_args = packages_isort_args + isort_args
    # packages
    process_files(filter(lambda f: 'var/spack/repos/builtin' in f, file_list),
                  packages_isort_args)
    # non-packages
    process_files(filter(lambda f: 'var/spack/repos/builtin' not in f, file_list),
                  isort_args)

    print_tool_result("isort", returncode[0])
    return returncode[0]


@tool("black")
def run_black(black_cmd, file_list, args):
    # always run with config from running spack prefix
    black_args = ("--config", os.path.join(spack.paths.prefix, "pyproject.toml"))
    if not args.fix:
        black_args += ("--check", "--diff")
        if color.get_color_when():  # only show color when spack would
            black_args += ("--color",)

    pat = re.compile("would reformat +(.*)")
    replacement = "would reformat {0}"
    returncode = 0
    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        packed_args = black_args + tuple(chunk)
        output = black_cmd(*packed_args, fail_on_error=False, output=str, error=str)
        returncode |= black_cmd.returncode

        rewrite_and_print_output(output, args, pat, replacement)

    print_tool_result("black", returncode)

    return returncode


def style(parser, args):
    # ensure python version is new enough
    if sys.version_info < (3, 6):
        tty.die("spack style requires Python 3.6 or later.")

    # save initial working directory for relativizing paths later
    args.initial_working_dir = os.getcwd()

    # ensure that the config files we need actually exist in the spack prefix.
    # assertions b/c users should not ever see these errors -- they're checked in CI.
    assert os.path.isfile(os.path.join(spack.paths.prefix, "pyproject.toml"))
    assert os.path.isfile(os.path.join(spack.paths.prefix, ".flake8"))

    # validate spack root if the user provided one
    args.root = os.path.realpath(args.root) if args.root else spack.paths.prefix
    spack_script = os.path.join(args.root, "bin", "spack")
    if not os.path.exists(spack_script):
        tty.die(
            "This does not look like a valid spack root.",
            "No such file: '%s'" % spack_script
        )

    file_list = args.files
    if file_list:

        def prefix_relative(path):
            return os.path.relpath(os.path.abspath(os.path.realpath(path)), args.root)

        file_list = [prefix_relative(p) for p in file_list]

    return_code = 0
    with working_dir(args.root):
        if not file_list:
            file_list = changed_files(args.base, args.untracked, args.all)
        print_style_header(file_list, args)

        commands = {}
        with spack.bootstrap.ensure_bootstrap_configuration():
            for tool_name, bootstrap_fn in tool_order:
                # Skip the tool if it was not requested
                if not getattr(args, tool_name):
                    continue

                commands[tool_name] = bootstrap_fn()

            for tool_name, bootstrap_fn in tool_order:
                # Skip the tool if it was not requested
                if not getattr(args, tool_name):
                    continue

                run_function, required = tools[tool_name]
                print_tool_header(tool_name)
                return_code |= run_function(commands[tool_name], file_list, args)

    if return_code == 0:
        tty.msg(color.colorize("@*{spack style checks were clean}"))
    else:
        tty.error(color.colorize("@*{spack style found errors}"))

    return return_code
