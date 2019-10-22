# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMklDnn(CMakePackage):
    """Intel(R) Math Kernel Library for Deep Neural Networks
    (Intel(R) MKL-DNN)."""

    homepage = "https://01.org/mkl-dnn"
    url      = "https://github.com/intel/mkl-dnn/archive/v0.19.tar.gz"

    version('1.0-pc2', sha256='fcc2d951f7170eade0cfdd0d8d1d58e3e7785bd326bca6555f3722f8cba71811')
    version('0.19',    sha256='ba39da6adb263df05c4ca2a120295641fc97be75b588922e4274cb628dbe1dcd', preferred=True)
    version('0.18.1',  sha256='fc7506701dfece9b03c0dc83d0cda9a44a5de17cdb54bc7e09168003f02dbb70')
    version('0.11', sha256='4cb4a85b05fe42aa527fd70a048caddcba9361f6d3d7bea9f33d74524e206d7d')
    version('0.10', sha256='59828764ae43f1151f77b8997012c52e0e757bc50af1196b86fce8934178c570')
    version('0.9',  sha256='8606a80851c45b0076f7d4047fbf774ce13d6b6d857cb2edf95c7e1fd4bca1c7')

    depends_on('intel-mkl')
