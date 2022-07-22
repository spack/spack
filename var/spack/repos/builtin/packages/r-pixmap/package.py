# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPixmap(RPackage):
    """Bitmap Images ("Pixel Maps").

    Functions for import, export, plotting and other manipulations of bitmapped
    images."""

    cran = "pixmap"

    version('0.4-12', sha256='893ba894d4348ba05e6edf9c1b4fd201191816b444a214f7a6b2c0a79b0a2aec')
    version('0.4-11', sha256='6fa010749a59cdf56aad9f81271473b7d55697036203f2cd5d81372bcded7412')
