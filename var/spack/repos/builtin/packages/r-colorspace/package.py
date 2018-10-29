# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RColorspace(RPackage):
    """Carries out mapping between assorted color spaces including RGB, HSV,
    HLS, CIEXYZ, CIELUV, HCL (polar CIELUV), CIELAB and polar CIELAB.
    Qualitative, sequential, and diverging color palettes based on HCL colors
    are provided."""

    homepage = "https://cran.r-project.org/web/packages/colorspace/index.html"
    url      = "https://cran.r-project.org/src/contrib/colorspace_1.3-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/colorspace"

    version('1.3-2', '63000bab81d995ff167df76fb97b2984')
    version('1.2-6', 'a30191e9caf66f77ff4e99c062e9dce1')
