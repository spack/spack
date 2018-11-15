# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libyogrt(AutotoolsPackage):
    """Your One Get Remaining Time Library."""

    homepage = "https://github.com/LLNL/libyogrt"
    url      = "https://github.com/LLNL/libyogrt/archive/1.20-6.tar.gz"

    version('1.20-6', '478f27512842cc5f2b74a0c22b851f60')
    version('1.20-5', 'd0fa6526fcd1f56ddb3d93f602ec72f7')
    version('1.20-4', '092bea10de22c505ce92aa07001decbb')
    version('1.20-3', 'd0507717009a5f8e2009e3b63594738f')
    version('1.20-2', '780bda03268324f6b5f72631fff6e6cb')
