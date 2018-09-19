##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
