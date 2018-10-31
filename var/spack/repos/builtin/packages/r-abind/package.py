# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAbind(RPackage):
    """Combine multidimensional arrays into a single array. This is a
    generalization of 'cbind' and 'rbind'. Works with vectors, matrices, and
    higher-dimensional arrays. Also provides functions 'adrop', 'asub', and
    'afill' for manipulating, extracting and replacing data in arrays."""

    homepage = "https://cran.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/abind_1.4-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/abind"

    version('1.4-3', '10fcf80c677b991bf263d38be35a1fc5')
