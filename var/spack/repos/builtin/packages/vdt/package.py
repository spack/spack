# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vdt(CMakePackage):
    """Vectorised math. A collection of fast and inline implementations of
    mathematical functions."""

    homepage = "https://github.com/dpiparo/vdt"
    url      = "https://github.com/dpiparo/vdt/archive/v0.3.9.tar.gz"

    version('0.3.9', '80a2d73a82f7ef8257a8206ca22dd145')
    version('0.3.8', '25b07c72510aaa95fffc11e33579061c')
    version('0.3.7', 'd2621d4c489894fd1fe8e056d9a0a67c')
    version('0.3.6', '6eaff3bbbd5175332ccbd66cd71a741d')
