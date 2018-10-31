# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRpart(RPackage):
    """Recursive partitioning for classification, regression and
    survival trees."""

    homepage = "https://cran.r-project.org/package=rpart"
    url      = "https://cran.r-project.org/src/contrib/rpart_4.1-10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rpart"

    version('4.1-11', 'f77b37cddf7e9a7b5993a52a750b8817')
    version('4.1-10', '15873cded4feb3ef44d63580ba3ca46e')

    depends_on('r@2.15.0:')
