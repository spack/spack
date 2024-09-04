# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fd(CargoPackage):
    """A simple, fast and user-friendly alternative to 'find'"""

    homepage = "https://github.com/sharkdp/fd"
    url = "https://github.com/sharkdp/fd/archive/refs/tags/v8.4.0.tar.gz"

    maintainers("alecbcs", "ashermancinelli")

    license("Apache-2.0 OR MIT")

    version("10.1.0", sha256="ee4b2403388344ff60125c79ff25b7895a170e7960f243ba2b5d51d2c3712d97")
    version("9.0.0", sha256="306d7662994e06e23d25587246fa3fb1f528579e42a84f5128e75feec635a370")
    version("8.7.0", sha256="13da15f3197d58a54768aaad0099c80ad2e9756dd1b0c7df68c413ad2d5238c9")
    version("8.4.0", sha256="d0c2fc7ddbe74e3fd88bf5bb02e0f69078ee6d2aeea3d8df42f508543c9db05d")
    version("7.4.0", sha256="33570ba65e7f8b438746cb92bb9bc4a6030b482a0d50db37c830c4e315877537")
