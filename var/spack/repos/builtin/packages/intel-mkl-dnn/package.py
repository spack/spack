# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMklDnn(CMakePackage):
    """Intel(R) Math Kernel Library for Deep Neural Networks
    (Intel(R) MKL-DNN)."""

    homepage = "https://01.org/mkl-dnn"
    url      = "https://github.com/01org/mkl-dnn/archive/v0.11.tar.gz"

    version('0.11', 'a060a42753f633a146c3db699eeee666')
    version('0.10', '3855ad02452a6906e3a9adc9cecef49c')
    version('0.9',  'dfb89d8f9d0bce55e878df32544cb0ea')

    depends_on('intel-mkl')
