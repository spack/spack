# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import platform
import sys

import spack_installable.main as sim

import llnl.util.tty as tty

import spack
import spack.paths
import spack.util.environment as sue
import spack.util.executable as exe

description = "launch an interpreter as spack would launch a command"
section = "developer"
level = "long"


def setup_parser(subparser):
    ex = subparser.add_mutually_exclusive_group()
    ex.add_argument(
        "-V",
        "--version",
        action="store_true",
        dest="python_version",
        help="print the Python version number and exit",
    )
    ex.add_argument(
        "--path",
        action="store_true",
        dest="show_path",
        help="show path to python interpreter that spack uses",
    )
    ex.add_argument("-c", dest="python_command", metavar="COMMAND", help="command to execute")
    ex.add_argument("-m", dest="module", action="store", help="run library module as a script")

    subparser.add_argument(
        "-i",
        dest="python_interpreter",
        help="python interpreter",
        choices=["python", "ipython"],
        default="python",
    )

    subparser.add_argument(
        "-I", dest="ipython", action="store_true", help="run with IPython instead of python"
    )

    subparser.add_argument(
        "python_args", nargs=argparse.REMAINDER, help="file to run plus arguments"
    )


def python(parser, args, unknown_args):
    if args.python_version:
        print("Python", platform.python_version())
        return

    if args.show_path:
        print(sys.executable)
        return

    # Unexpected behavior from supplying both
    if args.python_command and args.python_args:
        tty.die("You can only specify a command OR script, but not both.")

    # Run user choice of interpreter
    if args.python_interpreter == "ipython":
        tty.warn(
            "The `-i ipython` option is deprecated and will be removed in 0.21.", "Use -I instead."
        )
        args.ipython = True

    if args.ipython:
        return spack.cmd.python.ipython_interpreter(args, unknown_args)
    else:
        return spack.cmd.python.python_interpreter(args, unknown_args)


def construct_python_args(args, unknown_args):
    """Create python command args from argparse args."""
    python_args = []

    # add these two back as they're explicitly parsed
    if args.python_command:
        python_args += ["-c", args.python_command]
    if args.module:
        python_args += ["-m", args.module]

    python_args += unknown_args
    python_args += args.python_args
    return python_args


def print_spack_version_if_interactive(args):
    interactive = not any((args.python_command, args.python_args, args.module))
    if interactive:
        print(f"Spack version {spack.spack_version}")


def ipython_interpreter(args, unknown_args):
    """An ipython interpreter is intended to be interactive, so it doesn't
    support running a script or arguments
    """
    try:
        import IPython  # type: ignore[import]
    except ImportError:
        tty.die("IPython is not installed, install and try again.")

    print_spack_version_if_interactive(args)

    python_args = construct_python_args(args, unknown_args)
    IPython.start_ipython(argv=python_args)


def python_interpreter(args, unknown_args):
    """A python interpreter is the default interpreter"""
    # create a new environment for the spack python instance that sets PYTHONPATH to
    # include Spack packages.
    mods = sue.EnvironmentModifications()
    sys_paths = sim.get_spack_sys_paths(spack.paths.prefix)
    for path in reversed(sys_paths):
        mods.prepend_path("PYTHONPATH", path)

    env = os.environ.copy()
    mods.apply_modifications(env)

    print_spack_version_if_interactive(args)

    # note: this used to use code.InteractiveConsole, but exec'ing python and not using
    # interactive mode ensures that things like the __main__ module will be defined and
    # that multiprocessing will work.
    python_args = construct_python_args(args, unknown_args)
    python = exe.Executable(sys.executable)
    python(*python_args, env=env)
