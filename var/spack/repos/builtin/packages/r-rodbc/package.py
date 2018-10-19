# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRodbc(RPackage):
    """An ODBC database interface."""

    homepage = "https://cran.rstudio.com/web/packages/RODBC/"
    url      = "https://cran.rstudio.com/src/contrib/RODBC_1.3-13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RODBC/"

    version('1.3-13', 'c52ef9139c2ed85adc53ad6effa7d68e')

    depends_on('unixodbc')
