# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freefem(AutotoolsPackage):
    """FreeFEM is a popular 2D and 3D partial differential equations (PDE) solver.
    It allows you to easily implement your own physics modules using the provided
    FreeFEM language. FreeFEM offers a large list of finite elements, like the
    Lagrange, Taylor-Hood, etc., usable in the continuous and discontinuous
    Galerkin method framework.
    """

    homepage = "https://freefem.org"
    url      = "https://github.com/FreeFem/FreeFem-sources/archive/refs/tags/v4.10.zip"

    maintainers = ['corentin-dev']

    version('4.10',  sha256='b60a4a2b4b7a2c4c9753d9a2f5bf4735ddf81e26df39843c674cddce70fde588')
    version('4.9',   sha256='1f90a7b0790d78de07794e056b2d3943e4a738da4961ba67fbb815f7583b8018')
    version('4.8',   sha256='538437691c07ad151ea15857db4c253ef58090c7953c72ebe3b5a4a020efde55')
    version('4.7-1', sha256='9a34d46441c7fb23b423daa245c739298f84fbf735d264edac89b6362a7358a3')
    version('4.7',   sha256='2e0913090aa324aa2d5bc787a4030d9f90c6bd33d475a835cb9273629bd81dce')
    version('4.6',   sha256='c5ebae617f55c18b7c0b3e307b82060b925ef2dd1b936c4ac9d58296caf40f4e')
    version('4.5',   sha256='3863636f99537605070a18a6e77a0e8df6888d088968172fe5b2b1efd1ff190f')

    variant('mpi', default=False,
            description='Activate MPI support')
    variant('petsc', default=False,
            description='Compile with PETSc/SLEPc')

    depends_on('mpi', when='+mpi')
    depends_on('slepc', when='+petsc')

    # Patches to help configure find correctly MPI flags
    # when using full path for compilers.
    patch('acmpi.patch', when='@4.9', sha256='8157d89fc19227a555b54a4f2eb1c44da8aef3192077a6df2e88093b850f4c50')
    patch('acmpi4.8.patch', when='@:4.8', sha256='be84f7b1b8182ff0151c258056a09bda70d72a611b0a4da1fa1954df2e0fe84e')

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        autoreconf('-i')

    def configure_args(self):
        spec = self.spec
        options = ['--disable-mkl',
                   'CFLAGS=%s' % ' '.join(spec.compiler_flags['cflags']),
                   'FFLAGS=%s' % ' '.join(spec.compiler_flags['fflags']),
                   'CXXFLAGS=%s' % ' '.join(spec.compiler_flags['cxxflags'])]

        if '+petsc' in spec:
            options.append('--with-petsc=%s'
                           % spec['petsc'].prefix.lib.petsc.conf.petscvariables)
            options.append('--with-slepc-ldflags=%s'
                           % spec['slepc'].libs.ld_flags)
            options.append('--with-slepc-include=%s'
                           % spec['slepc'].headers.include_flags)
        else:
            options.append('--without-petsc')
            options.append('--without-slepc')

        return options
