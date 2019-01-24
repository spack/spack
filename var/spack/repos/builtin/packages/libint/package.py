# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libint(AutotoolsPackage):
    """Libint is a high-performance library for computing
    Gaussian integrals in quantum mechanics.
    """

    homepage = "https://github.com/evaleev/libint"
    url = "https://github.com/evaleev/libint/archive/v2.1.0.tar.gz"

    version('2.2.0', 'da37dab862fb0b97a7ed7d007695ef47')
    version('2.1.0', 'd0dcb985fe32ddebc78fe571ce37e2d6')
    version('1.1.6', '990f67b55f49ecc18f32c58da9240684')
    version('1.1.5', '379b7d0718ff398715d6898807adf628')

    # Build dependencies
    depends_on('autoconf@2.52:', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    # Libint 2 dependencies
    depends_on('boost', when='@2:')
    depends_on('gmp', when='@2:')

    def url_for_version(self, version):
        base_url = "https://github.com/evaleev/libint/archive"
        if version == Version('1.0.0'):
            return "{0}/LIBINT_1_00.tar.gz".format(base_url)
        elif version < Version('2.1.0'):
            return "{0}/release-{1}.tar.gz".format(base_url, version.dashed)
        else:
            return "{0}/v{1}.tar.gz".format(base_url, version)

    def autoreconf(self, spec, prefix):
        libtoolize()
        aclocal('-I', 'lib/autoconf')
        autoconf()

    @property
    def optflags(self):
        flags = '-O2'
        # Optimizations for the Intel compiler, suggested by CP2K
        # See ../libxc/package.py for rationale and doc.
        if '%intel' in self.spec:
            flags += ' -xSSE4.2 -axAVX,CORE-AVX2 -ipo'

        return flags

    def setup_environment(self, build_env, run_env):
        # Set optimization flags
        build_env.set('CFLAGS', self.optflags)
        build_env.set('CXXFLAGS', self.optflags)

        # Change AR to xiar if we compile with Intel and we
        # find the executable
        if '%intel' in self.spec and which('xiar'):
            build_env.set('AR', 'xiar')

    def configure_args(self):

        config_args = ['--enable-shared']

        optflags = self.optflags

        # Optimization flag names have changed in libint 2
        if self.version < Version('2.0.0'):
            config_args.extend([
                '--with-cc-optflags={0}'.format(optflags),
                '--with-cxx-optflags={0}'.format(optflags)
            ])
        else:
            config_args.extend([
                '--with-cxx-optflags={0}'.format(optflags),
                '--with-cxxgen-optflags={0}'.format(optflags)
            ])

        # Options required by CP2K, removed in libint 2
        if self.version < Version('2.0.0'):
            config_args.extend([
                '--with-libint-max-am=5',
                '--with-libderiv-max-am1=4'
            ])
        return config_args
