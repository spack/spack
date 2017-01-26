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

import argparse

import llnl.util.tty as tty
import spack.cmd
import spack.cmd.install as inst

from spack import *

description = 'stops at configuration stage when installing a package, if possible'  # NOQA: ignore=E501


build_system_to_phase = {
    CMakePackage: 'cmake',
    AutotoolsPackage: 'configure'
}


def setup_parser(subparser):
    subparser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )
    subparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="print additional output during builds"
    )


def _stop_at_phase_during_install(args, calling_fn, phase_mapping):
    if not args.package:
        tty.die("configure requires at least one package argument")

    # TODO: to be refactored with code in install
    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) != 1:
        tty.error('only one spec can be installed at a time.')
    spec = specs.pop()
    pkg = spec.package
    try:
        key = [cls for cls in phase_mapping if isinstance(pkg, cls)].pop()
        phase = phase_mapping[key]
        # Install package dependencies if needed
        parser = argparse.ArgumentParser()
        inst.setup_parser(parser)
        tty.msg('Checking dependencies for {0}'.format(args.package))
        cli_args = ['-v'] if args.verbose else []
        install_args = parser.parse_args(cli_args + ['--only=dependencies'])
        install_args.package = args.package
        inst.install(parser, install_args)
        # Install package and stop at the given phase
        cli_args = ['-v'] if args.verbose else []
        install_args = parser.parse_args(cli_args + ['--only=package'])
        install_args.package = args.package
        inst.install(parser, install_args, stop_at=phase)
    except IndexError:
        tty.error(
            'Package {0} has no {1} phase, or its {1} phase is not separated from install'.format(  # NOQA: ignore=E501
                spec.name, calling_fn.__name__)
        )


def configure(parser, args):
    _stop_at_phase_during_install(args, configure, build_system_to_phase)
