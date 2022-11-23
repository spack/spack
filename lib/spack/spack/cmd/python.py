# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import code
import os
import platform
import runpy
import sys

import llnl.util.tty as tty

import spack
import spack.paths
import spack.util.environment as sue
import spack.util.executable as exe

description = "launch an interpreter as spack would launch a command"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-V",
        "--version",
        action="store_true",
        dest="python_version",
        help="print the Python version number and exit",
    )
    subparser.add_argument("-c", dest="python_command", help="command to execute")
    subparser.add_argument(
        "-u",
        dest="unbuffered",
        action="store_true",
        help="for compatibility with xdist, do not use without adding -u to the interpreter",
    )
    subparser.add_argument(
        "-i",
        dest="python_interpreter",
        help="python interpreter",
        choices=["python", "ipython"],
        default="python",
    )
    subparser.add_argument(
        "-m", dest="module", action="store", help="run library module as a script"
    )
    subparser.add_argument(
        "--path",
        action="store_true",
        dest="show_path",
        help="show path to python interpreter that spack uses",
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

    if args.module:
        sys.argv = ["spack-python"] + unknown_args + args.python_args
        runpy.run_module(args.module, run_name="__main__", alter_sys=True)
        return

    if unknown_args:
        tty.die("Unknown arguments:", " ".join(unknown_args))

    # Unexpected behavior from supplying both
    if args.python_command and args.python_args:
        tty.die("You can only specify a command OR script, but not both.")

    # Run user choice of interpreter
    if args.python_interpreter == "ipython":
        return spack.cmd.python.ipython_interpreter(args)
    return spack.cmd.python.python_interpreter(args)


def ipython_interpreter(args):
    """An ipython interpreter is intended to be interactive, so it doesn't
    support running a script or arguments
    """
    try:
        import IPython  # type: ignore[import]
    except ImportError:
        tty.die("ipython is not installed, install and try again.")

    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with open(startup_file) as startup:
                exec(startup.read())

    # IPython can also support running a script OR command, not both
    if args.python_args:
        IPython.start_ipython(argv=args.python_args)
    elif args.python_command:
        IPython.start_ipython(argv=["-c", args.python_command])
    else:
        header = "Spack version %s\nPython %s, %s %s" % (
            spack.spack_version,
            platform.python_version(),
            platform.system(),
            platform.machine(),
        )

        __name__ = "__main__"  # noqa: F841
        IPython.embed(module="__main__", header=header)


def python_interpreter(args):
    """A python interpreter is the default interpreter"""
    if args.python_command or args.python_args:
        # create a new environment for the spack python instance that sets PYTHONPATH to
        # include Spack packages.
        mods = sue.EnvironmentModifications()
        mods.prepend_path("PYTHONPATH", spack.paths.lib_path)
        mods.prepend_path("PYTHONPATH", spack.paths.external_path)

        env = os.environ.copy()
        mods.apply_modifications(env)

        # if we're not running an interactive console, exec python and don't bother with
        # an interactive interpreter, since that means things like the __main__ module
        # will not be defined, and multiprocessing won't work.
        python_args = []
        if args.python_command:
            python_args += ["-c", args.python_command]
        if args.python_args:
            python_args += args.python_args

        python = exe.Executable(sys.executable)
        python(*python_args, env=env)

    else:
        # if we're running interactively, use InteractiveConsole and set up a little
        # readline help.
        console = code.InteractiveConsole({"spack": spack})
        if "PYTHONSTARTUP" in os.environ:
            startup_file = os.environ["PYTHONSTARTUP"]
            if os.path.isfile(startup_file):
                with open(startup_file) as startup:
                    console.runsource(startup.read(), startup_file, "exec")

        # Provides readline support, allowing user to use arrow keys
        console.push("import readline")
        # Provide tabcompletion
        console.push("from rlcompleter import Completer")
        console.push("readline.set_completer(Completer(locals()).complete)")
        console.push('readline.parse_and_bind("tab: complete")')

        console.interact(
            "Spack version %s\nPython %s, %s %s"
            % (
                spack.spack_version,
                platform.python_version(),
                platform.system(),
                platform.machine(),
            )
        )
