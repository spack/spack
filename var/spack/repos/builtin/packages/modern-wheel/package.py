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
from spack import *
import sys


class ModernWheel(CMakePackage):
    """C++ utility collection. Provides various facilities of common use in
    modern codebases like dynamic linking helpers, loadable plugins facilities
    and misc patterns."""

    homepage = "https://github.com/alalazo/modern_wheel"
    url      = "https://github.com/alalazo/modern_wheel/archive/1.2.tar.gz"

    version('1.2', 'dc440099c52b6af3b8ddff6fd7730aff')
    version('1.1', '289455239ad19497b7db55aacb299ca8')
    version('1.0', '503dc3e7da2b422c4295e4afcba09dfb')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    # Test implementation files cause some issues on darwin,
    # needs to be investigated.
    variant('test',   default=sys.platform != 'darwin',
            description='Enables the build of unit tests')

    # FindBoost shipped with CMake up to version 3.10.2 (latest one
    # up to now) is known to be unable to detect Boost >= 1.66.0.
    # This issue will be probably fixed in CMake >= 3.11.0:
    # https://gitlab.kitware.com/cmake/cmake/issues/17575
    # Until then, just assume that we cannot correctly configure
    # ModernWheel with Boost >= 1.66.0.
    depends_on('boost           +system +filesystem', when='@:1.1.999')
    depends_on('boost@:1.65.999 +system +filesystem', when='@1.2:')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_UNIT_TEST:BOOL={0}'.format(
                'ON' if '+test' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
        ]
