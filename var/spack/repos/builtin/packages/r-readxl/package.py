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
    url      = "https://cloud.r-project.org/src/contrib/readxl_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/readxl"

    version('1.3.1', sha256='24b441713e2f46a3e7c6813230ad6ea4d4ddf7e0816ad76614f33094fbaaaa96')
    version('1.3.0', sha256='8379d1026dcfc662d073eb1c69ed1d90aa6439d6cb3c6fc1b5d1db4f51b3fadc')
    version('1.1.0', sha256='b63d21fc6510acb373e96deaec45e966a523ec75cbec75a089529297ed443116')
    version('1.0.0', '030c47ae1af5dd4168087160c29131e4')

    depends_on('r-tibble@1.3.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.18:', type=('build', 'run'))
    depends_on('r-cellranger', type=('build', 'run'))
    depends_on('r-progress', when='@1.2.0:', type=('build', 'run'))
