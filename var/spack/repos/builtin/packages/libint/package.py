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

    version('2.4.2', sha256='86dff38065e69a3a51d15cfdc638f766044cb87e5c6682d960c14f9847e2eac3')
    version('2.4.1', sha256='0513be124563fdbbc7cd3c7043e221df1bda236a037027ba9343429a27db8ce4')
    version('2.4.0', sha256='52eb16f065406099dcfaceb12f9a7f7e329c9cfcf6ed9bfacb0cff7431dd6019')
    version('2.2.0', sha256='f737d485f33ac819d7f28c6ce303b1f3a2296bfd2c14f7c1323f8c5d370bb0e3')
    version('2.1.0', sha256='43c453a1663aa1c55294df89ff9ece3aefc8d1bbba5ea31dbfe71b2d812e24c8')
    version('1.1.6', sha256='f201b0c621df678cfe8bdf3990796b8976ff194aba357ae398f2f29b0e2985a6')
    version('1.1.5', sha256='ec8cd4a4ba1e1a98230165210c293632372f0e573acd878ed62e5ec6f8b6174b')

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
