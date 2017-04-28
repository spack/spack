##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import os
import argparse

import llnl.util.tty as tty
import spack.cmd
import spack.build_environment as build_env

description = "run a command with the install environment for a spec"


def setup_parser(subparser):
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs of package environment to emulate")


def env(parser, args):
    if not args.spec:
        tty.die("spack env requires a spec.")

    # Specs may have spaces in them, so if they do, require that the
    # caller put a '--' between the spec and the command to be
    # executed.  If there is no '--', assume that the spec is the
    # first argument.
    sep = '--'
    if sep in args.spec:
        s = args.spec.index(sep)
        spec = args.spec[:s]
        cmd  = args.spec[s + 1:]
    else:
        spec = args.spec[0]
        cmd  = args.spec[1:]

    specs = spack.cmd.parse_specs(spec, concretize=True)
    if len(specs) > 1:
        tty.die("spack env only takes one spec.")
    spec = specs[0]

    build_env.setup_package(spec.package)

    if not cmd:
        # If no command act like the "env" command and print out env vars.
        for key, val in os.environ.items():
            print("%s=%s" % (key, val))

    else:
        # Otherwise execute the command with the new environment
        os.execvp(cmd[0], cmd)
