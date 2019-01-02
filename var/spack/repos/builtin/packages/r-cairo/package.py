# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCairo(RPackage):
    """R graphics device using cairo graphics library for creating high-quality
       bitmap (PNG, JPEG, TIFF), vector (PDF, SVG, PostScript) and display
       (X11 and Win32) output"""

    homepage = "https://cran.r-project.org/web/packages/Cairo/index.html"
    url      = "https://cran.r-project.org/src/contrib/Cairo_1.5-9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Cairo"

    version('1.5-9', '2a867b6cae96671d6bc3acf9334d6615dc01f6ecf1953a27cde8a43c724a38f4')

    depends_on('cairo@1.2:')
