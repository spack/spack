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


class RRinside(RPackage):
    """C++ classes to embed R in C++ applications The 'RInside' packages makes
    it easier to have "R inside" your C++ application by providing a C++
    wrapperclass providing the R interpreter. As R itself is embedded into
    your application, a shared library build of R is required. This works on
    Linux, OS X and even on Windows provided you use the same tools used to
    build R itself. Numerous examples are provided in the eight subdirectories
    of the examples/ directory of the installed package: standard, mpi (for
    parallel computing) qt (showing how to embed 'RInside' inside a Qt GUI
    application), wt (showing how to build a "web-application" using the Wt
    toolkit), armadillo (for 'RInside' use with 'RcppArmadillo') and eigen (for
    'RInside' use with 'RcppEigen'). The example use GNUmakefile(s) with GNU
    extensions, so a GNU make is required (and will use the GNUmakefile
    automatically). Doxygen-generated documentation of the C++ classes is
    available at the 'RInside' website as well."""

    homepage = "http://dirk.eddelbuettel.com/code/rinside.html"
    url      = "https://cran.r-project.org/src/contrib/RInside_0.2.14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RInside"

    version('0.2.14', 'fc72761e22b1f597433eb53d6eb122ff')
    version('0.2.13', '2e3c35a7bd648e9bef98d0afcc02cf88')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
