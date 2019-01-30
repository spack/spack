# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGetoptlong(RPackage):
    """This is yet another command-line argument parser which wraps the
       powerful Perl module Getopt::Long and with some adaptation for easier
       use in R. It also provides a simple way for variable interpolation in
       R."""

    homepage = "https://cran.rstudio.com/web/packages/GetoptLong/index.html"
    url      = "https://cran.rstudio.com/src/contrib/GetoptLong_0.1.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/GetoptLong"

    version('0.1.6', 'e4b964d0817cb6c6a707297b21405749')

    depends_on('r-rjson', type=('build', 'run'))
    depends_on('r-globaloptions', type=('build', 'run'))
    depends_on('perl')
