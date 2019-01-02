# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReadxl(RPackage):
    """Import excel files into R. Supports '.xls' via the embedded
    'libxls' C library <https://sourceforge.net/projects/libxls/> and
    '.xlsx' via the embedded 'RapidXML' C++ library
    <https://rapidxml.sourceforge.net>. Works on Windows, Mac and Linux
    without external dependencies."""

    homepage = "http://readxl.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/readxl_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/readxl/readxl_1.0.0.tar.gz"

    version('1.1.0', sha256='b63d21fc6510acb373e96deaec45e966a523ec75cbec75a089529297ed443116')
    version('1.0.0', '030c47ae1af5dd4168087160c29131e4')

    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-cellranger', type=('build', 'run'))
