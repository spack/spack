# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Sirius(CMakePackage):
    """Domain specific library for electronic structure calculations"""

    homepage = "https://github.com/electronic-structure/SIRIUS"
    url      = "https://github.com/electronic-structure/SIRIUS/archive/v6.1.5.tar.gz"
    list_url = "https://github.com/electronic-structure/SIRIUS/releases"

    version('6.1.5', sha256='379f0a2e5208fd6d91c2bd4939c3a5c40002975fb97652946fa1bfe4a3ef97cb')

    variant('shared', default=False, description="Build shared libraries")
    variant('openmp', default=True, description="Build with OpenMP support")
    variant('fortran', default=False, description="Build Fortran bindings")
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

    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('libvdwxc+mpi', when='+vdwxc')
    depends_on('scalapack', when='+scalapack')

    # TODO:
    # add support for MKL, CUDA, MAGMA, CRAY_LIBSCI, Python bindings, testing

    patch("strip-spglib-include-subfolder.patch")
    patch("link-libraries-fortran.patch")

    @property
    def libs(self):
        libraries = []

        if self.spec.satisfies('+fortran'):
            libraries += ['libsirius_f']

        return find_libraries(
            libraries, root=self.prefix,
            shared=self.spec.satisfies('+shared'), recursive=True
        )

    def cmake_args(self):
        def _def(variant, flag=None):
            """Returns "-DUSE_VARIANT:BOOL={ON,OFF}" depending on whether
               +variant is set. If the CMake flag differs from the variant
               name, pass the flag name explicitly.
            """

            return "-D{0}:BOOL={1}".format(
                flag if flag else "USE_{0}".format(
                    variant.strip('+~').upper()
                ),
                "ON" if self.spec.satisfies(variant) else "OFF"
            )

        args = [
            '-DBUILD_SHARED_LIBS=ON',
            _def('+openmp'),
            _def('+elpa'),
            _def('+vdwxc'),
            _def('+scalapack'),
            _def('+fortran', 'CREATE_FORTRAN_BINDINGS'),
        ]

        if self.spec.satisfies('+elpa'):
            elpa_incdir = os.path.join(
                self.spec['elpa'].headers.directories[0],
                'elpa'
            )
            args += ["-DELPA_INCLUDE_DIR={0}".format(elpa_incdir)]

        return args
