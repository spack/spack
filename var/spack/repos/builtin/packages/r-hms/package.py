# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHms(RPackage):
    """Implements an S3 class for storing and formatting time-of-day values,
       based on the 'difftime' class."""

    homepage = "https://cran.rstudio.com/web/packages/hms/index.html"
    url      = "https://cran.rstudio.com/src/contrib/hms_0.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/hms"

    version('0.5.0', sha256='a87872665c3bf3901f597d78c152e7805f7129e4dbe27397051de4cf1a76561b')
    version('0.3', '92c4a0cf0c402a35145b5bb57212873e')
