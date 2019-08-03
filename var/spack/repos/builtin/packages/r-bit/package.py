# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBit(RPackage):
    """ A class for vectors of 1-bit booleans."""

    homepage = "https://cran.rstudio.com/web/packages/bit/index.html"
    url      = "https://cran.rstudio.com/src/contrib/bit_1.1-12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bit"

    version('1.1-14', sha256='5cbaace1fb643a665a6ca69b90f7a6d624270de82420ca7a44f306753fcef254')
    version('1.1-12', 'c4473017beb93f151a8e672e4d5747af')
