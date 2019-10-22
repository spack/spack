# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty
import spack.cmd
import spack.cmd.install as inst

from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.intel import IntelPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.sip import SIPPackage

description = 'stage and configure a package but do not install'
section = "build"
level = "long"


build_system_to_phase = {
    AutotoolsPackage: 'configure',
    CMakePackage: 'cmake',
    QMakePackage: 'qmake',
    WafPackage: 'configure',
    PerlPackage: 'configure',
    IntelPackage: 'configure',
    MesonPackage: 'meson',
    SIPPackage: 'configure',
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
        tty.msg('Checking dependencies for {0}'.format(args.package[0]))
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
