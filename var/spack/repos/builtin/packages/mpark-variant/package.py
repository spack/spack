# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MparkVariant(CMakePackage):
    """C++17 `std::variant` for C++11/14/17"""

    homepage = "https://mpark.github.io/variant"
    url      = "https://github.com/mpark/variant/archive/v1.3.0.tar.gz"
    maintainers = ['ax3l']

    version('1.3.0', '368b7d6f1a07bd6ee26ff518258dc71c')

    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.5')
