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


class Libxc(AutotoolsPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "http://www.tddft.org/programs/octopus/wiki/index.php/Libxc"
    url      = "http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz"

    version('3.0.0', '8227fa3053f8fc215bd9d7b0d36de03c')
    version('2.2.2', 'd9f90a0d6e36df6c1312b6422280f2ec')
    version('2.2.1', '38dc3a067524baf4f8521d5bb1cd0b8f')

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
            libraries = ['libxcf90'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    def setup_environment(self, spack_env, run_env):
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
