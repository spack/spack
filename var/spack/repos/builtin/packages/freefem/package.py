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
    url      = "https://github.com/FreeFem/FreeFem-sources/archive/refs/tags/v4.10.tar.gz"

    maintainers = ['corentin-dev']

    version('4.10',  sha256='b60a4a2b4b7a2c4c9753d9a2f5bf4735ddf81e26df39843c674cddce70fde588')
    version('4.9',   sha256='299ba2b73dfff578b7890f693c1e835680bf55eba87263cabd60d81909e1e0e4')
    version('4.8',   sha256='499b1ca24d45088226a238412ea1492d9cc3eb6088866904145511469780180d')
    version('4.7-1', sha256='60d84424d20b5f6abaee638dc423480fc76f9c389bba1a2f23fd984e39a3fb96')
    version('4.7',   sha256='c1797b642e9c3d543eaad4949d26ce1e986f531ee9be14fff606ea525ada9206')
    version('4.6',   sha256='6c09af8e189fc02214b0e664b679b49832c134e29cf1ede3cab29cf754f6078f')
    version('4.5',   sha256='5b2d4125c312da8fbedd49a72e742f18f35e0ae100c82fb493067dfad5d51432')

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
