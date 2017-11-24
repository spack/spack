##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
from spack.build_systems.cuda import CudaPackage


class Bohrium(CMakePackage, CudaPackage):
    """Library for automatic acceleration of array operations"""

    homepage    = "http://bh107.org"
    url         = "https://github.com/bh107/bohrium/archive/v0.8.9.tar.gz"
    maintainers = ['mfherbst']

    #
    # Versions
    #
    version("develop", git="https://github.com/bh107/bohrium.git",
            branch="master")

    #
    # Variants
    #
    variant("cuda", default=True,
            description="Build with CUDA code generator")
    variant('opencl', default=True,
            description="Build with OpenCL code generator")
    variant('openmp', default=True,
            description="Build with OpenMP code generator")

    variant('node', default=True,
            description="Build the node vector engine manager")
    variant('proxy', default=True,
            description="Build the proxy vector engine manager")
    variant('python', default=True,
            description="Build the numpy-like bridge "
            "to enable use from python")
    variant('cbridge', default=True,
            description="Build the bridge interface towards plain C")

    variant('blas', default=True,
            description="Build with BLAS extension methods")
    variant('lapack', default=True,
            description="Build with LAPACK extension methods")

    #
    # Conflicts and extensions
    #
    conflicts('%intel')
    conflicts('%clang@:3.5')
    extends('python', when="+python")

    # Bohrium needs at least one vector engine and
    # at least one vector engine manager
    conflicts('~node~proxy')
    conflicts('~openmp~opencl~cuda')

    #
    # Dependencies
    #
    depends_on('cmake@2.8:', type="build")
    depends_on('boost+system+serialization+filesystem+regex')

    # cuda dependencies managed by CudaPackage class
    depends_on('opencl', when="+opencl")

    # NOTE The lapacke interface and hence netlib-lapack
    #      is the strictly required lapack provider
    #      for bohrium right now.
    depends_on("netlib-lapack+lapacke", when="+lapack")
    depends_on("blas", when="+blas")

    depends_on('python', type="build", when="~python")
    depends_on('python', when="+python")
    depends_on('py-numpy', when="+python")
    depends_on('swig', type="build", when="+python")
    depends_on('py-cython', type="build", when="+python")

    depends_on('zlib', when="+proxy")

    #
    # Settings and cmake cache
    #
    def cmake_args(self):
        spec = self.spec

        cuda_arch = spec.variants['cuda_arch'].value
        if "+cuda" in spec and len(cuda_arch) >= 1 and cuda_arch[0]:
            # TODO Add cuda_arch support to Bohrium once the basic setup
            #      via Spack works.
            raise InstallError(
                "Bohrium does not support setting the CUDA architecture yet."
            )

        args = [
            "-DPYTHON_EXECUTABLE:FILEPATH=" + spec['python'].command.path,
            # Hard-disable Jupyter, since this would override a config
            # file in the user's home directory in some cases during
            # the configuration stage.
            "-DJUPYTER_FOUND=FALSE",
            "-DJUPYTER_EXECUTABLE=FALSE",
            #
            # Vector engine managers
            "-DVEM_NODE=" + str("+node" in spec),
            "-DVEM_PROXY=" + str("+proxy" in spec),
            #
            # Vector engines
            "-DVE_OPENMP=" + str("+openmp" in spec),
            "-DVE_OPENCL=" + str("+opencl" in spec),
            "-DVE_CUDA=" + str("+cuda" in spec),
            #
            # Bridges and interfaces
            "-DBRIDGE_BHXX=ON",
            "-DBRIDGE_C=" + str("+cbridge" in spec or "+python" in spec),
            "-DBRIDGE_NPBACKEND=" + str("+python" in spec),
            "-DNO_PYTHON3=ON",  # Only build python version we provide
        ]

        #
        # Extension methods
        #
        if "+blas" in spec:
            args += [
                "-DEXT_BLAS=ON",
                "-DCBLAS_FOUND=True",
                "-DCBLAS_LIBRARIES=" + ";".join(spec["blas"].libs),
                "-DCBLAS_INCLUDES=" + spec["blas"].prefix.include,
            ]
        else:
            args += ["-DEXT_BLAS=OFF", "-DDCBLAS_FOUND=False"]

        if "+lapack" in spec:
            args += [
                "-DEXT_LAPACK=ON",
                "-DLAPACKE_FOUND=True",
                "-DLAPACKE_LIBRARIES=" + ";".join(spec["lapack"].libs),
                "-DLAPACKE_INCLUDE_DIR=" + spec["lapack"].prefix.include,
            ]
        else:
            args += ["-DEXT_LAPACK=OFF", "-DLAPACKE_FOUND=False"]

        # TODO Other extension methods are not ready yet, because of missing
        #      packages or because they are untested, so disable in order
        #      to prevent their setup:
        args += [
            "-DEXT_LAPACK=" + str("+lapack" in spec),
            "-DEXT_CLBLAS=OFF",      # clBLAS not in Spack yet
            "-DEXT_TDMA=OFF",        # untested
            "-DEXT_VISUALIZER=OFF",  # untested
            "-DEXT_OPENCV=OFF",      # untested
        ]

        return args

    #
    # Environment setup
    #
    def setup_environment(self, spack_env, run_env):
        # Bohrium needs an extra include dir apart from
        # the self.prefix.include dir
        run_env.prepend_path("CPATH", self.prefix.include.bohrium)
