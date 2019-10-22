# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Sirius(CMakePackage, CudaPackage):
    """Domain specific library for electronic structure calculations"""

    homepage = "https://github.com/electronic-structure/SIRIUS"
    url      = "https://github.com/electronic-structure/SIRIUS/archive/v6.1.5.tar.gz"
    list_url = "https://github.com/electronic-structure/SIRIUS/releases"

    version('6.1.5', sha256='379f0a2e5208fd6d91c2bd4939c3a5c40002975fb97652946fa1bfe4a3ef97cb')
    version('6.3.2', sha256='1723e5ad338dad9a816369a6957101b2cae7214425406b12e8712c82447a7ee5')

    variant('shared', default=False, description="Build shared libraries")
    variant('openmp', default=True, description="Build with OpenMP support")
    variant('fortran', default=False, description="Build Fortran bindings")
    variant('python', default=False, description="Build Python bindings")
    variant('elpa', default=False, description="Use ELPA")
    variant('vdwxc', default=False, description="Enable libvdwxc support")
    variant('scalapack', default=False, description="Enable scalapack support")

    depends_on('python')
    depends_on('mpi')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('fftw')  # SIRIUS does not care about MPI-support in FFTW
    depends_on('libxc')
    depends_on('spglib')
    depends_on('hdf5+hl')
    depends_on('pkgconfig', type='build')
    depends_on('py-mpi4py', when='+python')
    depends_on('py-pybind11', when='+python')

    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('libvdwxc+mpi', when='+vdwxc')
    depends_on('scalapack', when='+scalapack')
    depends_on('cuda', when='+cuda')

    conflicts('+shared', when='@6.3.0:')  # option to build shared libraries has been removed

    # TODO:
    # add support for MAGMA, CRAY_LIBSCI, ROCm, testing

    patch("strip-spglib-include-subfolder.patch", when='@6.1.5')
    patch("link-libraries-fortran.patch", when='@6.1.5')
    patch("cmake-fix-shared-library-installation.patch", when='@6.1.5')

    @property
    def libs(self):
        libraries = []

        if '@6.3.0:' in self.spec:
            libraries += ['libsirius']

            return find_libraries(
                libraries, root=self.prefix,
                shared=False, recursive=True
            )

        else:
            if '+fortran' in self.spec:
                libraries += ['libsirius_f']

            if '+cuda' in self.spec:
                libraries += ['libsirius_cu']

            return find_libraries(
                libraries, root=self.prefix,
                shared='+shared' in self.spec, recursive=True
            )

    def cmake_args(self):
        spec = self.spec

        def _def(variant, flag=None):
            """Returns "-DUSE_VARIANT:BOOL={ON,OFF}" depending on whether
               +variant is set. If the CMake flag differs from the variant
               name, pass the flag name explicitly.
            """

            return "-D{0}:BOOL={1}".format(
                flag if flag else "USE_{0}".format(
                    variant.strip('+~').upper()
                ),
                "ON" if variant in spec else "OFF"
            )

        args = [
            _def('+openmp'),
            _def('+elpa'),
            _def('+vdwxc'),
            _def('+scalapack'),
            _def('+fortran', 'CREATE_FORTRAN_BINDINGS'),
            _def('+python', 'CREATE_PYTHON_MODULE'),
            _def('+cuda')
        ]

        if '@:6.2.999' in self.spec:
            args += [_def('+shared', 'BUILD_SHARED_LIBS')]

        lapack = spec['lapack']
        blas = spec['blas']

        args += [
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES={0}'.format(lapack.libs.joined(';')),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES={0}'.format(blas.libs.joined(';')),
        ]

        if '+scalapack' in spec:
            args += [
                '-DSCALAPACK_FOUND=true',
                '-DSCALAPACK_INCLUDE_DIRS={0}'.format(
                    spec['scalapack'].prefix.include),
                '-DSCALAPACK_LIBRARIES={0}'.format(
                    spec['scalapack'].libs.joined(';')),
            ]

        if spec['blas'].name in ['intel-mkl', 'intel-parallel-studio']:
            args += ['-DUSE_MKL=ON']

        if '+elpa' in spec:
            elpa_incdir = os.path.join(
                spec['elpa'].headers.directories[0],
                'elpa'
            )
            args += ["-DELPA_INCLUDE_DIR={0}".format(elpa_incdir)]

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch:
                args += [
                    '-DCMAKE_CUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0])
                ]

        return args
