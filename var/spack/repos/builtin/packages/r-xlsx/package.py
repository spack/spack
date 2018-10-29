# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXlsx(RPackage):
    """Provide R functions to read/write/format Excel 2007 and Excel
    97/2000/XP/2003 file formats."""

    homepage = "http://code.google.com/p/rexcel/"
    url      = "https://cran.rstudio.com/src/contrib/xlsx_0.5.7.tar.gz"

    version('0.5.7', '36b1b16f29c54b6089b1dae923180dd5')

    depends_on('r-rjava', type=('build', 'run'))
    depends_on('r-xlsxjars', type=('build', 'run'))
