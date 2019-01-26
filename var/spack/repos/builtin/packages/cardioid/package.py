# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cardioid
#
# You can edit this file again by typing:
#
#     spack edit cardioid
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import spack.environment as ev
import os


class Cardioid(CMakePackage):
    """Cardiac simulation suite."""

    git = "https://github.com/LLNL/cardioid.git"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('master', branch='master')
    version('elecfem', branch='elec-fem')

    variant('cuda', default=False, 
            description='Build with cuda support')
    variant('mfem', default=False,
            description='Build with mfem support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('cuda', when="+cuda")
    depends_on('mfem+hypre+superlu-dist+lapack', when="+mfem~cuda")
    depends_on('mfem+hypre+superlu-dist+lapack^hypre+cuda', when="+mfem+cuda")
    depends_on('cmake@3.1:', type='build')
    depends_on('perl', type='build')

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        env = ev.get_env(None, 'env status')
        if not env:
            basename = str(self.spec.arch)
        else:
            basename = env.name

        return os.path.join(self.stage.source_path, "build", basename)

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DLAPACK_LIB:PATH=" + ";".join(spec['lapack'].libs.libraries),
            "-DBLAS_LIB:PATH=" + ";".join(spec['blas'].libs.libraries),
            "-DENABLE_OPENMP:BOOL=ON",

            "-DENABLE_MPI:BOOL=ON",
            "-DENABLE_FIND_MPI:BOOL=OFF",
            "-DMPI_C_COMPILER:STRING=" + spec['mpi'].mpicc,
            "-DMPI_CXX_COMPILER:STRING=" + spec['mpi'].mpicxx,
            "-DCMAKE_C_COMPILER:STRING=" + spec['mpi'].mpicc,
            "-DCMAKE_CXX_COMPILER:STRING=" + spec['mpi'].mpicxx,
        ]

        if "+cuda" in self.spec:
            args.append("-DENABLE_CUDA:BOOL=ON")
            args.append("-DCUDA_TOOLKIT_ROOT:PATH=" + spec['cuda'].prefix)
        else:
            args.append("-DENABLE_CUDA:BOOL=OFF")

        if "+mfem" in self.spec:
            args.append("-DMFEM_DIR:PATH=" + spec['mfem'].prefix)
        return args
