# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROptparse(RPackage):
    """A command line parser inspired by Python's 'optparse' library to be used
       with Rscript to write "#!" shebang scripts that accept short and long
       flag/options"""

    homepage = "https://cran.r-project.org/package=optparse"
    url      = "https://cran.r-project.org/src/contrib/optparse_1.6.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/optparse"

    version('1.6.0', '8d0bd89b2e25cc1580437cdeeb1faac2')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-getopt@1.20.2:', type=('build', 'run'))
