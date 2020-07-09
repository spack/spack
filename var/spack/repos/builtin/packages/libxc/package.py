# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxc(AutotoolsPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "https://tddft.org/programs/libxc/"
    url      = "https://www.tddft.org/programs/libxc/down.php?file=2.2.2/libxc-2.2.2.tar.gz"

    version('4.3.2', sha256='bc159aea2537521998c7fb1199789e1be71e04c4b7758d58282622e347603a6f')
    version('4.2.3', sha256='02e49e9ba7d21d18df17e9e57eae861e6ce05e65e966e1e832475aa09e344256')
    version('3.0.0', sha256='5542b99042c09b2925f2e3700d769cda4fb411b476d446c833ea28c6bfa8792a')
    version('2.2.2', sha256='6ca1d0bb5fdc341d59960707bc67f23ad54de8a6018e19e02eee2b16ea7cc642')
    version('2.2.1', sha256='ade61c1fa4ed238edd56408fd8ee6c2e305a3d5753e160017e2a71817c98fd00')

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

    def setup_build_environment(self, env):
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
                env.set('AR', 'xiar')

        env.append_flags('CFLAGS',  optflags)
        env.append_flags('FCFLAGS', optflags)

    def configure_args(self):
        args = ['--enable-shared']
        return args

    def check(self):
        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        pass
