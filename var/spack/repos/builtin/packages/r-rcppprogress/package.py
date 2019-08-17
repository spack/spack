# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppprogress(RPackage):
    """Allows to display a progress bar in the R console for long running
    computations taking place in c++ code, and support for interrupting
    those computations even in multithreaded code, typically using OpenMP."""

    homepage = "https://cran.r-project.org/web/packages/RcppProgress/index.html"
    url      = "https://cran.r-project.org/src/contrib/RcppProgress_0.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RcppProgress"

    version('0.3',   '3cd527af84bc6fcb3c77422e0ff09dba')
    version('0.2.1', 'c9cd69759ff457acfee0b52353f9af1b')
    version('0.2',   '9522c962ecddd4895b5636e7a499bda5')
    version('0.1',   '34afefe0580ca42b6353533fe758d5bf')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-rcpp', type=('build', 'run'))
