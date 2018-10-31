# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIterators(RPackage):
    """Support for iterators, which allow a programmer to traverse through all
    the elements of a vector, list, or other collection of data."""

    homepage = "https://cran.r-project.org/web/packages/iterators/index.html"
    url      = "https://cran.r-project.org/src/contrib/iterators_1.0.8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/iterators"

    version('1.0.8', '2ded7f82cddd8174f1ec98607946c6ee')
