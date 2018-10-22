# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RForeach(RPackage):
    """Support for the foreach looping construct. Foreach is an idiom that
    allows for iterating over elements in a collection, without the use of an
    explicit loop counter. This package in particular is intended to be used
    for its return value, rather than for its side effects. In that sense, it
    is similar to the standard lapply function, but doesn't require the
    evaluation of a function. Using foreach without side effects also
    facilitates executing the loop in parallel."""

    homepage = "https://cran.r-project.org/web/packages/foreach/index.html"
    url      = "https://cran.r-project.org/src/contrib/foreach_1.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/foreach"

    version('1.4.3', 'ef45768126661b259f9b8994462c49a0')

    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
