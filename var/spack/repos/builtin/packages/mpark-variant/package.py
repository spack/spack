# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MparkVariant(CMakePackage):
    """C++17 `std::variant` for C++11/14/17"""

    homepage = "https://mpark.github.io/variant"
    url      = "https://github.com/mpark/variant/archive/v1.3.0.tar.gz"
    maintainers = ['ax3l']

    version('1.4.0', sha256='8f6b28ab3640b5d76d5b6664dda7257a4405ce59179220431b8fd196c79b2ecb')
    version('1.3.0', sha256='d0f7e41f818fcc839797a8017e76b8b66b323651c304cff641a83a56ae9943c6')

    # Ref.: https://github.com/mpark/variant/pull/73
    patch('nvcc.patch', when='@:1.4.0')

    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.5')
