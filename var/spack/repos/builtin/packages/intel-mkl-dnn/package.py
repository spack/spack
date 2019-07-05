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
    version('0.11', 'a060a42753f633a146c3db699eeee666')
    version('0.10', '3855ad02452a6906e3a9adc9cecef49c')
    version('0.9',  'dfb89d8f9d0bce55e878df32544cb0ea')

    depends_on('intel-mkl')
