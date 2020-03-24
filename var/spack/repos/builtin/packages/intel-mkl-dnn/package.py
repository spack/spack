# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMklDnn(CMakePackage):
    """Intel(R) Math Kernel Library for Deep Neural Networks
    (Intel(R) MKL-DNN)."""

    homepage = "https://intel.github.io/mkl-dnn/"
    url      = "https://github.com/intel/mkl-dnn/archive/v1.2.2.tar.gz"

    maintainers = ['adamjstewart']

    version('1.2.2',  sha256='a71ec1f27c30b8a176605e8a78444f1f12301a3c313b70ff93290926c140509c')
    version('1.2.1',  sha256='c69544783c453ab3fbf14c7a5b9a512561267690c9fc3e7fc3470f04756e0ab3')
    version('1.2',    sha256='30979a09753e8e35d942446c3778c9f0eba543acf2fb0282af8b9c89355d0ddf')
    version('1.1.3',  sha256='0e9bcbc86cc215a84a5455a395ce540c68e255eaa586e37222fff622b9b17df7')
    version('1.1.2',  sha256='284b20e0cab67025bb7d21317f805d6217ad77fb3a47ad84b3bacf37bde62da9')
    version('1.1.1',  sha256='a31b08a89473bfe3bd6ed542503336d21b4177ebe4ccb9a97810808f634db6b6')
    version('1.1',    sha256='c5aac67e5ed4d95fe9943f835df49bbe6d608507780787c64aa620bdbd2171ba')
    version('1.0.4',  sha256='2a3ca90a8b690e65ddd0ccc95a09818e6da439cc854d014367645fcfd58a9690')
    version('1.0.3',  sha256='e0de341bd0bbebde7637e69383899ba415ce67682ff2f0f3d5a0d268e1bea69b')
    version('1.0.2',  sha256='3164eb2914e2160ac6ffd345781cf7554ce410830398cc6b2761e8668faf5ca8')
    version('1.0.1',  sha256='91fb84601c18f8a5a87eccd7b63d61f03495f36c5c533bd7f59443e4f8bb2595')
    version('1.0',    sha256='27fd9da9720c452852f1226581e7914efcf74e1ff898468fdcbe1813528831ba')
    version('0.21.4', sha256='1e774138203b773b5af2eed9cc6f1973f13a7263a3b80127682246c5a6c5bc45')
    version('0.21.3', sha256='31e78581e59d7e60d4becaba3834fc6a5bf2dccdae3e16b7f70d89ceab38423f')
    version('0.21.2', sha256='ed56652dd237deb86ee9bf102c18de5f2625c059e5ab1d7512c8dc01e316b694')
    version('0.21.1', sha256='766ecfa5ac68be8cf9eacd4c712935c0ed945e5e6fe51640f05ee735cff62a38')
    version('0.21',   sha256='eb0aff133134898cf173d582a90e39b90ea9ea59544de7914208c2392b51a15f')
    version('0.20.6', sha256='74675e93eef339ff3d9a9be95c15d0c7ad8736a5356c23428ab2e33dcdb8e3e1')
    version('0.20.5', sha256='081d9f853c00fe0b597c8f00f2f3ff8d79c2a9cb95f292ff2c90557709763021')
    version('0.20.4', sha256='b6422a000a6754334bdae673c25f84efd95e6d3cd016b752145b9391dc13e729')
    version('0.20.3', sha256='a198a9bd3c584607e6a467f780beca92c8411cd656fcc8ec6fa5abe73d4af823')
    version('0.20.2', sha256='1ae0e8a1a3df58deadc08ca0a01f8d3720600b26ca9e53685493e8e8250243b2')
    version('0.20.1', sha256='26f720ed912843ba293e8a1e0822fe5318e93c529d80c87af1cf555d68e642d0')
    version('0.20',   sha256='52e111fefbf5a38e36f7bae7646860f7cbc985eba0725768f3fee8cdb31a9977')
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
