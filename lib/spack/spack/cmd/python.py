# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
import code
import argparse
import platform
import runpy

import llnl.util.tty as tty

import spack

description = "launch an interpreter as spack would launch a command"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-c', dest='python_command', help='command to execute')
    subparser.add_argument(
        '-m', dest='module', action='store',
        help='run library module as a script')
    subparser.add_argument(
        'python_args', nargs=argparse.REMAINDER,
        help="file to run plus arguments")


def python(parser, args, unknown_args):
    if args.module:
        sys.argv = ['spack-python'] + unknown_args + args.python_args
        runpy.run_module(args.module, run_name="__main__", alter_sys=True)
        return

    if unknown_args:
        tty.die("Unknown arguments:", " ".join(unknown_args))

    # Fake a main python shell by setting __name__ to __main__.
    console = code.InteractiveConsole({'__name__': '__main__',
                                       'spack': spack})

    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with open(startup_file) as startup:
                console.runsource(startup.read(), startup_file, 'exec')

    python_args = args.python_args
    python_command = args.python_command
    if python_command:
        console.runsource(python_command)
    elif python_args:
        sys.argv = python_args
        with open(python_args[0]) as file:
            console.runsource(file.read(), python_args[0], 'exec')
    else:
        # Provides readline support, allowing user to use arrow keys
        console.push('import readline')

        console.interact("Spack version %s\nPython %s, %s %s"""
                         % (spack.spack_version, platform.python_version(),
                            platform.system(), platform.machine()))
