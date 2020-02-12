# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import os

import llnl.util.tty as tty
import spack.build_environment as build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
from spack.util.environment import dump_environment, pickle_environment

description = "run a command in a spec's install environment, " \
              "or dump its environment to screen or file"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['clean', 'dirty'])
    subparser.add_argument(
        '--dump', metavar="FILE",
        help="dump a source-able environment to FILE"
    )
    subparser.add_argument(
        '--pickle', metavar="FILE",
        help="dump a pickled source-able environment to FILE"
    )
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        metavar='spec [--] [cmd]...',
        help="spec of package environment to emulate")
    subparser.epilog\
        = 'If a command is not specified, the environment will be printed ' \
        'to standard output (cf /usr/bin/env) unless --dump and/or --pickle ' \
        'are specified.\n\nIf a command is specified and spec is ' \
        'multi-word, then the -- separator is obligatory.'


def build_env(parser, args):
    if not args.spec:
        tty.die("spack build-env requires a spec.")

    # Specs may have spaces in them, so if they do, require that the
    # caller put a '--' between the spec and the command to be
    # executed.  If there is no '--', assume that the spec is the
    # first argument.
    sep = '--'
    if sep in args.spec:
        s = args.spec.index(sep)
        spec = args.spec[:s]
        cmd = args.spec[s + 1:]
    else:
        spec = args.spec[0]
        cmd = args.spec[1:]

    specs = spack.cmd.parse_specs(spec, concretize=True)
    if len(specs) > 1:
        tty.die("spack build-env only takes one spec.")
    spec = specs[0]

    build_environment.setup_package(spec.package, args.dirty)

    if args.dump:
        # Dump a source-able environment to a text file.
        tty.msg("Dumping a source-able environment to {0}".format(args.dump))
        dump_environment(args.dump)

    if args.pickle:
        # Dump a source-able environment to a pickle file.
        tty.msg(
            "Pickling a source-able environment to {0}".format(args.pickle))
        pickle_environment(args.pickle)

    if cmd:
        # Execute the command with the new environment
        os.execvp(cmd[0], cmd)

    elif not bool(args.pickle or args.dump):
        # If no command or dump/pickle option act like the "env" command
        # and print out env vars.
        for key, val in os.environ.items():
            print("%s=%s" % (key, val))
