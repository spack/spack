# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lynx(AutotoolsPackage):
    """Lynx is the text web browser."""

    homepage = "https://lynx.invisible-island.net/"
    url      = "https://invisible-mirror.net/archives/lynx/tarballs/lynx2.8.9rel.1.tar.gz"

    version('2.8.9rel.1', sha256='a46e4167b8f02c066d2fe2eafcc5603367be0e3fe2e59e9fc4eb016f306afc8e')
    version('2.8.8rel.1', sha256='28cdb16136eea8ca097d2994138519bfbbdfe63b7d10fee6a4908580e5f55fc5')
    version('2.8.7rel.1', sha256='6570e3088c0ae22fbd48a528f4841a1f2b83f588c7d31c059c3bbbcd5c7e7298')

    depends_on('ncurses')
