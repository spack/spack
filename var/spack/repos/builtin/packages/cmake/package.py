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


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
       tools designed to build, test and package software."""
    homepage = 'https://www.cmake.org'
    url      = 'https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz'
    list_url = 'https://cmake.org/files/'
    list_depth = 1

    version('3.12.1',   '10109246a51102bfda45ff3935275fbf')
    version('3.12.0',   'ab4aa7df9301c94cdd6f8ee4fe66458b')
    version('3.11.4',   '72e168b3bad2f9c34dcebbad7af56ff0')
    version('3.11.3',   '3f923154ed47128f13b08eacd207d9ee')
    version('3.11.2',   'd2d554c05fc07cfae7846d2aa205f12a')
    version('3.11.1',   '12a3177477e4e2c7bc514193d421dafe')
    version('3.11.0',   'f3ebc79b5dec85b49abe75958ffa1a03')
    version('3.10.3',   '1c38c67295ca696aeafd8c059d748b38')
    version('3.10.2',   '732808e17fc14dc8cee50d51518c34eb')
    version('3.10.1',   '9a726e5ec69618b172aa4b06d18c3998')
    version('3.10.0',   'f3f8e70ca3055f3cd288f89ff233057e')
    version('3.9.6',    '084b1c8b2efc1c1ba432dea37243c0ae')
    version('3.9.4',    '33769e001bdcd788f565bf378692e5ae')
    version('3.9.0',    '180e23b4c9b55915d271b315297f6951')
    version('3.8.2',    'b5dff61f6a7f1305271ab3f6ae261419')
    version('3.8.1',    'e8ef820ddf7a650845252bca846696e7')
    version('3.8.0',    'f28cba717ba38ad82a488daed8f45b5b')
    version('3.7.2',    '79bd7e65cd81ea3aa2619484ad6ff25a')
    version('3.7.1',    'd031d5a06e9f1c5367cdfc56fbd2a1c8')
    version('3.6.1',    'd6dd661380adacdb12f41b926ec99545')
    version('3.6.0',    'aa40fbecf49d99c083415c2411d12db9')
    version('3.5.2',    '701386a1b5ec95f8d1075ecf96383e02')
    version('3.5.1',    'ca051f4a66375c89d1a524e726da0296')
    version('3.5.0',    '33c5d09d4c33d4ffcc63578a6ba8777e')
    version('3.4.3',    '4cb3ff35b2472aae70f542116d616e63')
    version('3.4.0',    'cd3034e0a44256a0917e254167217fc8')
    version('3.3.1',    '52638576f4e1e621fed6c3410d3a1b12')
    version('3.1.0',    '188eb7dc9b1b82b363bc51c0d3f1d461')
    version('3.0.2',    'db4c687a31444a929d2fdc36c4dfb95f')
    version('2.8.10.2', '097278785da7182ec0aea8769d06860c')

    variant('ownlibs', default=True,  description='Use CMake-provided third-party libraries')
    variant('qt',      default=False, description='Enables the build of cmake-gui')
    variant('doc',     default=False, description='Enables the generation of html and man page documentation')
    variant('openssl', default=True,  description="Enables CMake's OpenSSL features")
    variant('ncurses', default=True,  description='Enables the build of the ncurses gui')

    depends_on('curl',           when='~ownlibs')
    depends_on('expat',          when='~ownlibs')
    # depends_on('jsoncpp',        when='~ownlibs')  # circular dependency
    depends_on('zlib',           when='~ownlibs')
    depends_on('bzip2',          when='~ownlibs')
    depends_on('xz',             when='~ownlibs')
    depends_on('libarchive',     when='~ownlibs')
    depends_on('libuv@1.0.0:',   when='~ownlibs')
    depends_on('rhash',          when='@3.8.0:~ownlibs')
    depends_on('qt',             when='+qt')
    depends_on('python@2.7.11:', when='+doc', type='build')
    depends_on('py-sphinx',      when='+doc', type='build')
    depends_on('openssl', when='+openssl')
    depends_on('openssl@:1.0.99', when='@:3.6.9+openssl')
    depends_on('ncurses',        when='+ncurses')

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch('intel-c-gnu11.patch', when='@3.6.0:3.6.1')

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch('nag-response-files.patch', when='@3.7:3.12')

    conflicts('+qt', when='^qt@5.4.0')  # qt-5.4.0 has broken CMake modules

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts('%intel', when='@3.11.0:3.11.4')

    phases = ['bootstrap', 'build', 'install']

    def url_for_version(self, version):
        """Handle CMake's version-based custom URLs."""
        url = 'https://cmake.org/files/v{0}/cmake-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    def bootstrap_args(self):
        spec = self.spec
        args = [
            '--prefix={0}'.format(self.prefix),
            '--parallel={0}'.format(make_jobs)
        ]

        if '+ownlibs' in spec:
            # Build and link to the CMake-provided third-party libraries
            args.append('--no-system-libs')
        else:
            # Build and link to the Spack-installed third-party libraries
            args.append('--system-libs')

            if spec.satisfies('@3.2:'):
                # jsoncpp requires CMake to build
                # use CMake-provided library to avoid circular dependency
                args.append('--no-system-jsoncpp')

        if '+qt' in spec:
            args.append('--qt-gui')
        else:
            args.append('--no-qt-gui')

        if '+doc' in spec:
            args.append('--sphinx-html')
            args.append('--sphinx-man')

        if '+openssl' in spec:
            args.append('--')
            args.append('-DCMAKE_USE_OPENSSL=ON')

        return args

    def bootstrap(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap(*self.bootstrap_args())

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test(self):
        # Some tests fail, takes forever
        make('test')

    def install(self, spec, prefix):
        make('install')
