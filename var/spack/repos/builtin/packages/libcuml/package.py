# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcuml(CMakePackage):
    """cuML is a suite of libraries that implement machine
    learning algorithms and mathematical primitives functions
    that share compatible APIs with other RAPIDS projects."""

    homepage = "https://rapids.ai"
    url      = "https://github.com/rapidsai/cuml/archive/v0.15.0.tar.gz"

    version('0.15.0',  sha256='b6b37c0f370cd4e881fc24083166ee86a934f1b823159ad36fac6457412c79cd')

    depends_on('cmake@3.14:', type='build')
    depends_on('zlib')
    depends_on('libcudf@0.8:')
    depends_on('cuda@9.2:')
    depends_on('blas')
    depends_on('nccl@2.4:')
    depends_on('treelite')
    depends_on('googletest')
    depends_on('libcumlprims')
    depends_on('mpi')

    root_cmakelists_dir = 'cpp'

    def cmake_args(self):
        args = []

        #-DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
        #-DCMAKE_CXX11_ABI=${BUILD_ABI} \
        #-DBLAS_LIBRARIES=${INSTALL_PREFIX}/lib/libopenblas.so.0 \
        #${GPU_ARCH} \
        #-DCMAKE_BUILD_TYPE=${BUILD_TYPE}
        #-DBUILD_CUML_MG_TESTS=${BUILD_CPP_MG_TESTS}
        #-DPARALLEL_LEVEL=${PARALLEL_LEVEL}
        #-DDISABLE_DEPRECATION_WARNING=${BUILD_DISABLE_DEPRECATION_WARNING}
        #-DCMAKE_PREFIX_PATH=${INSTALL_PREFIX}
        args.append("-DNCCL_PATH={0}".format(self.spec['nccl'].prefix))
        args.append("-DBUILD_CUML_C_LIBRARY=ON")
        args.append("-DWITH_UCX=ON")
        args.append("-DNVTX=OFF")
        args.append("-DBUILD_STATIC_FAISS=ON")
        args.append("-DSINGLEGPU=OFF")
        args.append("-DENABLE_CUMLPRIMS_MG=ON")
        args.append("-DBUILD_CUML_MPI_COMMS=ON")

        return args
