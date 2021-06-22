# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zziplib(AutotoolsPackage, CMakePackage):
    """The zziplib provides read access to zipped files in a zip-archive, using
    compression based solely on free algorithms provided by zlib.  It also
    provides a functionality to overlay the archive filesystem with the
    filesystem of the operating system environment."""

    homepage = "https://github.com/gdraheim/zziplib"
    url      = "https://github.com/gdraheim/zziplib/archive/v0.13.69.tar.gz"

    # Switch to CMake from 0.13.70, first working release is 0.13.71
    version('0.13.72', sha256='93ef44bf1f1ea24fc66080426a469df82fa631d13ca3b2e4abaeab89538518dc')
    version('0.13.69', sha256='846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544')

    patch('python2to3.patch', when='@:0.13.69')

    build_directory = 'spack-build'

    depends_on('python@3.5:', type='build', when='@0.13.71:')
    depends_on('cmake', type='build', when='@0.13.71:')
    depends_on('python', type='build')
    depends_on('zlib')
    # see zzip/CMakeLists.txt
    depends_on('coreutils', type='build', when='@0.13.71:')
    depends_on('pkgconfig', type='build', when='@0.13.71:')

    # configure phase stands for cmake since 0.13.70
    phases = ['configure', 'build', 'install']

    @when('@0.13.71:')
    def _cmake_args(self):
        spec = self.spec
        args = []
        zlib = spec['zlib']
        args.extend([
            self.define('ZLIB_LIBRARY', zlib.libs[0]),
            self.define('ZLIB_INCLUDE_DIR', zlib.headers.directories[0]),
        ])
        args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s'
                    % spec['python'].command.path)
        args.append("-DCMAKE_INSTALL_PREFIX:PATH={0}".format(spec.prefix))

        return args

    @when('@:0.13.70')
    def configure_args(self):
        if '@:0.13.70' in self.spec:
            args = ['--with-zlib={0}'.format(self.spec['zlib'].prefix)]
            return args

    @when('@0.13.71:')
    def configure(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = self._cmake_args()
            cmake('..', *cmake_args)
