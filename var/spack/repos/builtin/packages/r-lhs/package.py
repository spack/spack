# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLhs(RPackage):
    """Provides a number of methods for creating and augmenting Latin Hypercube
       Samples."""

    homepage = "http://lhs.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/lhs_0.16.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lhs"

    version('0.16', '088e593e5283414951e7e541a50ec2d1')
