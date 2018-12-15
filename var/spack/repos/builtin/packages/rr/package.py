# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
