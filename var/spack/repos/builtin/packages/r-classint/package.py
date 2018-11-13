# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClassint(RPackage):
    """Selected commonly used methods for choosing univariate class intervals
       for mapping or other graphics purposes."""

    homepage = "https://cran.r-project.org/package=classInt"
    url      = "https://cran.r-project.org/src/contrib/classInt_0.1-24.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/classInt"

    version('0.1-24', '45f1bde3ec7601ce17c99189be5c0fd5')

    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
