# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBit(RPackage):
    """ A class for vectors of 1-bit booleans."""

    homepage = "https://cran.rstudio.com/web/packages/bit/index.html"
    url      = "https://cran.rstudio.com/src/contrib/bit_1.1-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bit"
    version('1.1-12', 'c4473017beb93f151a8e672e4d5747af')
