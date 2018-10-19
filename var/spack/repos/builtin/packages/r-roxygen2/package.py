# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRoxygen2(RPackage):
    """A 'Doxygen'-like in-source documentation system for Rd, collation, and
    'NAMESPACE' files."""

    homepage = "https://github.com/klutometis/roxygen"
    url      = "https://cran.r-project.org/src/contrib/roxygen2_5.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/roxygen2"

    version('5.0.1', 'df5bdbc12fda372e427710ef1cd92ed7')

    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-brew', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
