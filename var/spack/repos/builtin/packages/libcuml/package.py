# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install libcuml
#
# You can edit this file again by typing:
#
#     spack edit libcuml
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libcuml(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/rapidsai/cuml/archive/v0.15.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.15.0',  sha256='b6b37c0f370cd4e881fc24083166ee86a934f1b823159ad36fac6457412c79cd')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('cmake@3.14:', type='build')
    depends_on('zlib')
    depends_on('libcudf@0.8:')
    depends_on('cuda@9.2:')
    depends_on('blas')
    depends_on('nccl@2.4:')
    depends_on('treelite')
    depends_on('googletest')

    root_cmakelists_dir = 'cpp'

    build_targets = [ 'cuml++', 'cuml', 'ml', 'prims' ]

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []

        #-DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
        #-DCMAKE_CXX11_ABI=${BUILD_ABI} \
        #-DBLAS_LIBRARIES=${INSTALL_PREFIX}/lib/libopenblas.so.0 \
        #${GPU_ARCH} \
        #-DCMAKE_BUILD_TYPE=${BUILD_TYPE}
        #-DBUILD_CUML_MPI_COMMS=${BUILD_CPP_MG_TESTS}
        #-DBUILD_CUML_MG_TESTS=${BUILD_CPP_MG_TESTS}
        #-DPARALLEL_LEVEL=${PARALLEL_LEVEL}
        #-DDISABLE_DEPRECATION_WARNING=${BUILD_DISABLE_DEPRECATION_WARNING}
        #-DCMAKE_PREFIX_PATH=${INSTALL_PREFIX}
        args.append("-DNCCL_PATH={0}".format(self.spec['nccl'].prefix))
        args.append("-DBUILD_CUML_C_LIBRARY=ON")
        args.append("-DWITH_UCX=ON")
        args.append("-DNVTX=OFF")
        # FIXME
        args.append("-DENABLE_CUMLPRIMS_MG=OFF")
        args.append("-DBUILD_STATIC_FAISS=ON")
        args.append("-DSINGLEGPU=ON")

        return args
