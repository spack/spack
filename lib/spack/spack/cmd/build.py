# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.cmd.configure as cfg

from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.sip import SIPPackage

description = 'stops at build stage when installing a package, if possible'
section = "build"
level = "long"


build_system_to_phase = {
    AutotoolsPackage: 'build',
    CMakePackage: 'build',
    QMakePackage: 'build',
    SConsPackage: 'build',
    WafPackage: 'build',
    PythonPackage: 'build',
    PerlPackage: 'build',
    MesonPackage: 'build',
    SIPPackage: 'build',
}


def setup_parser(subparser):
    cfg.setup_parser(subparser)


def build(parser, args):
    cfg._stop_at_phase_during_install(args, build, build_system_to_phase)
