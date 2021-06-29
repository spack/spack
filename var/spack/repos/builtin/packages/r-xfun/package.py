# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXfun(RPackage):
    """Miscellaneous functions commonly used in other packages maintained by
    'Yihui Xie'."""

    homepage = "https://github.com/yihui/xfun"
    cran     = "xfun"

    version('0.24', sha256='e3e39a95202f6db4f6de3a8b9a344074a4944a3a8a522d44971390c905e2b583')
    version('0.20', sha256='284239d12a3d5ea7d1ef8b1382fb0a7a4661af54c85510501279681871da7c10')
    version('0.8', sha256='c2f8ecf8b57ddec02f9be7f417d9e22fc1ae2c7db8d70aa703fc62bf4a5c5416')
