# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RColorspace(RPackage):
    """Carries out mapping between assorted color spaces including RGB, HSV,
    HLS, CIEXYZ, CIELUV, HCL (polar CIELUV), CIELAB and polar CIELAB.
    Qualitative, sequential, and diverging color palettes based on HCL colors
    are provided."""

    homepage = "https://cloud.r-project.org/package=colorspace"
    url      = "https://cloud.r-project.org/src/contrib/colorspace_1.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/colorspace"

    version('1.4-1', sha256='693d713a050f8bfecdb7322739f04b40d99b55aed168803686e43401d5f0d673')
    version('1.4-0', sha256='ce003c5958dd704697959e9dc8a108c8cb568f8d78ece113235732afc5dff556')
    version('1.3-2', '63000bab81d995ff167df76fb97b2984')
    version('1.2-6', 'a30191e9caf66f77ff4e99c062e9dce1')

    depends_on('r@3.0.0:', type=('build', 'run'))
