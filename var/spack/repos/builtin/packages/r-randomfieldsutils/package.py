# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRandomfieldsutils(RPackage):
    """Various utilities are provided that might be used in spatial statistics
       and elsewhere. It delivers a method for solving linear equations that
       checks the sparsity of the matrix before any algorithm is used.
       Furthermore, it includes the Struve functions."""

    homepage = "https://cran.r-project.org/web/packages/RandomFieldsUtils"
    url = "https://cran.r-project.org/src/contrib/RandomFieldsUtils_0.3.25.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils"

    version('0.3.25', '026c15a23296c9726012135891f016d5')

    depends_on('r@3.3:', type=('build', 'run'))
