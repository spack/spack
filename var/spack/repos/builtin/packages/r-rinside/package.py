# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    url      = "https://cloud.r-project.org/src/contrib/RInside_0.2.15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RInside"

    version('0.2.15', '3b8c13dc53c6958c1f82c0a25dd6c211')
    version('0.2.14', 'fc72761e22b1f597433eb53d6eb122ff')
    version('0.2.13', '2e3c35a7bd648e9bef98d0afcc02cf88')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
