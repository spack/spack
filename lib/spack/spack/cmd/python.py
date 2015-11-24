##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import sys
import code
import argparse
import platform

import spack

def setup_parser(subparser):
    subparser.add_argument(
        'python_args', nargs=argparse.REMAINDER, help="File to run plus arguments.")

description = "Launch an interpreter as spack would launch a command"

def python(parser, args):
    # Fake a main python shell by setting __name__ to __main__.
    console = code.InteractiveConsole({'__name__' : '__main__'})

    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with open(startup_file) as startup:
                console.runsource(startup.read(), startup_file, 'exec')

    python_args = args.python_args
    if python_args:
        sys.argv = python_args
        with open(python_args[0]) as file:
            console.runsource(file.read(), python_args[0], 'exec')
    else:
        console.interact("Spack version %s\nPython %s, %s %s"""
                         % (spack.spack_version, platform.python_version(),
                            platform.system(), platform.machine()))
