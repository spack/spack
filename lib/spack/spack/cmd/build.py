##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import spack.cmd.configure as cfg

from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.meson import MesonPackage

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
}


def setup_parser(subparser):
    cfg.setup_parser(subparser)


def build(parser, args):
    cfg._stop_at_phase_during_install(args, build, build_system_to_phase)
