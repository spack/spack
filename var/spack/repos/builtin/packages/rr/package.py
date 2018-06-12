##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
from spack import *


class Rr(CMakePackage):
    """Application execution recorder, player and debugger"""
    homepage = "http://rr-project.org/"
    url      = "https://github.com/mozilla/rr/archive/4.5.0.tar.gz"

    version('4.5.0', '1ec0aed0559b81143f59a200eeb302ef')
    version('4.4.0', '6d1cbb4fafbf6711114369907cf1efb1')
    version('4.3.0', '31470564e8b7eb317f619e4ef2244082')

    depends_on('gdb')
    depends_on('git')
    depends_on('zlib')
    # depends_on('capnproto', when='@4.6:')  # not yet in spack
    # depends_on('libcapnp')    # needed for future releases
    depends_on('pkgconfig', type='build')
    depends_on('py-pexpect', type='test')

    # rr needs architecture Nehalem and beyond, how can spack
    # test this?

    # Only 'Release' is supported at the moment
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Release'))

    def patch(self):
        # because otherwise CMake would try and fail to set RPATH of
        # rr_exec_stub
        filter_file(
            r'^(install\(TARGETS .*)\s*rr_exec_stub', r'\1', 'CMakeLists.txt')

    def cmake_args(self):
        return ['-Ddisable32bit=ON']

    @run_after('install')
    def install_stub(self):
        with working_dir(self.build_directory):
            mkdirp(self.prefix.bin)
            install('bin/rr_exec_stub', self.prefix.bin)
