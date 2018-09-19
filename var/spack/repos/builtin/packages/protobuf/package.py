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
import sys
from spack import *
import spack.util.web


class Protobuf(CMakePackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url      = "https://github.com/google/protobuf/archive/v3.2.0.tar.gz"
    root_cmakelists_dir = "cmake"

    version('3.5.2', 'ff6742018c172c66ecc627029ad54280')
    version('3.5.1.1', '5005003ae6b94773c4bbca87a644b131')
    version('3.5.1',   '710f1a75983092c9b45ecef207236104')
    version('3.5.0.1', 'b3ed2401acf167207277b254fd7f9638')
    version('3.5.0',   'd95db321e1a9901fffc51ed8994afd36')
    version('3.4.1',   '31b19dcfd6567095fdb66a8c07347222')
    version('3.4.0', '1d077a7d4db3d75681f5c333f2de9b1a')
    version('3.3.0', 'f0f712e98de3db0c65c0c417f5e7aca8')
    version('3.2.0', 'efaa08ae635664fb5e7f31421a41a995')
    version('3.1.0', '39d6a4fa549c0cce164aa3064b1492dc')
    version('3.0.2', '7349a7f43433d72c6d805c6ca22b7eeb')
    # does not build with CMake:
    # version('2.5.0', '9c21577a03adc1879aba5b52d06e25cf')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    depends_on('zlib')

    conflicts('%gcc@:4.6')  # Requires c++11

    # first fixed in 3.4.0: https://github.com/google/protobuf/pull/3406
    patch('pkgconfig.patch', when='@:3.3.2')

    patch('intel_inline.patch', when='@3.2.0: %intel')

    def fetch_remote_versions(self):
        """Ignore additional source artifacts uploaded with releases,
           only keep known versions
           fix for https://github.com/spack/spack/issues/5356"""
        return dict(map(
            lambda u: (u, self.url_for_version(u)),
            spack.util.web.find_versions_of_archive(
                self.all_urls, self.list_url, self.list_depth)
        ))

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS=%s' % int('+shared' in self.spec),
            '-Dprotobuf_BUILD_TESTS:BOOL=OFF',
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON'
        ]
        if sys.platform == 'darwin':
            args.extend(['-DCMAKE_MACOSX_RPATH=ON'])
        return args
