# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMklDnn(CMakePackage):
    """Intel(R) Math Kernel Library for Deep Neural Networks
    (Intel(R) MKL-DNN)."""

    homepage = "https://intel.github.io/mkl-dnn/"
    url      = "https://github.com/intel/mkl-dnn/archive/v1.1.1.tar.gz"

    maintainers = ['adamjstewart']

    version('1.1.1',  sha256='a31b08a89473bfe3bd6ed542503336d21b4177ebe4ccb9a97810808f634db6b6')
    version('0.19',   sha256='ba39da6adb263df05c4ca2a120295641fc97be75b588922e4274cb628dbe1dcd')
    version('0.18.1', sha256='fc7506701dfece9b03c0dc83d0cda9a44a5de17cdb54bc7e09168003f02dbb70')
    version('0.11',   sha256='4cb4a85b05fe42aa527fd70a048caddcba9361f6d3d7bea9f33d74524e206d7d')
    version('0.10',   sha256='59828764ae43f1151f77b8997012c52e0e757bc50af1196b86fce8934178c570')
    version('0.9',    sha256='8606a80851c45b0076f7d4047fbf774ce13d6b6d857cb2edf95c7e1fd4bca1c7')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('intel-mkl')
    depends_on('llvm-openmp', when='%clang platform=darwin')

    def cmake_args(self):
        args = []

        # https://github.com/intel/mkl-dnn/issues/591
        if self.spec.satisfies('%clang platform=darwin'):
            args.extend([
                '-DOpenMP_CXX_FLAGS={0}'.format(self.compiler.openmp_flag),
                '-DOpenMP_C_FLAGS={0}'.format(self.compiler.openmp_flag),
                '-DOpenMP_CXX_LIB_NAMES=libomp',
                '-DOpenMP_C_LIB_NAMES=libomp',
                '-DOpenMP_libomp_LIBRARY={0}'.format(
                    self.spec['llvm-openmp'].libs.libraries[0]
                ),
                '-DCMAKE_SHARED_LINKER_FLAGS={0}'.format(
                    self.spec['llvm-openmp'].libs.ld_flags
                ),
            ])

        return args
