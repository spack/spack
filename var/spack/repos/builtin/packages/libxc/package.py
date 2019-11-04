# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxc(AutotoolsPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "https://gitlab.com/libxc"
    url      = "https://gitlab.com/libxc/libxc/-/archive/2.2.2/libxc-2.2.2.tar.gz"

    version('4.3.4', sha256='2d5878dd69f0fb68c5e97f46426581eed2226d1d86e3080f9aa99af604c65647')
    version('4.3.2', sha256='3bbe01971d0a43fb63b5c17d922388a39a3f0ae3bd37ae5f6fe31bca9ab63f3c')
    version('4.2.3', sha256='869ca4967cd255097fd2dc31664f30607e81f5abcf5f9c89bd467dc0bf93e5aa')
    version('3.0.0', sha256='df2362351280edaf2233f3b2c8eb8e6dd6c68105f152897a4cc629fa346a7396')
    version('2.2.2', sha256='6ffaad40505dbe8f155049448554b54ea31d31babf74ccf6b7935bfe55eeafd8')
    version('2.2.1', sha256='c8577ba1ddd5c28fd0aa7c579ae65ab990eb7cb51ecf9f8175f9251f6deb9a06')

    depends_on('autoconf', type='build')

    @property
    def libs(self):
        """Libxc can be queried for the following parameters:

        - "static": returns the static library version of libxc
            (by default the shared version is returned)

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ['libxc']

        # Libxc installs both shared and static libraries.
        # If a client ask for static explicitly then return
        # the static libraries
        shared = ('static' not in query_parameters)

        # Libxc has a fortran90 interface: give clients the
        # possibility to query for it
        if 'fortran' in query_parameters:
            if self.version < Version('4.0.0'):
                libraries = ['libxcf90'] + libraries
            else:  # starting from version 4 there is also a stable f03 iface
                libraries = ['libxcf90', 'libxcf03'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autoreconf', '-i')

    def setup_build_environment(self, spack_env):
        optflags = '-O2'
        if self.compiler.name == 'intel':
            # Optimizations for the Intel compiler, suggested by CP2K
            #
            # Note that not every lowly login node has advanced CPUs:
            #
            #   $ icc  -xAVX -axCORE-AVX2 -ipo hello.c
            #   $ ./a.out
            #   Please verify that both the operating system and the \
            #   processor support Intel(R) AVX instructions.
            #
            # NB: The same flags are applied in:
            #   - ../libint/package.py
            #
            # Related:
            #   - ../fftw/package.py        variants: simd, fma
            #   - ../c-blosc/package.py     variant:  avx2
            #   - ../r-rcppblaze/package.py AVX* in "info" but not in code?
            #   - ../openblas/package.py    variants: cpu_target!?!
            #   - ../cp2k/package.py
            #
            # Documentation at:
            # https://software.intel.com/en-us/cpp-compiler-18.0-developer-guide-and-reference-ax-qax
            #
            optflags += ' -xSSE4.2 -axAVX,CORE-AVX2 -ipo'
            if which('xiar'):
                spack_env.set('AR', 'xiar')

        spack_env.append_flags('CFLAGS',  optflags)
        spack_env.append_flags('FCFLAGS', optflags)

    def configure_args(self):
        args = ['--enable-shared']
        return args

    def check(self):
        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        pass
