# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RTestit(RPackage):
    """Provides two convenience functions assert() and test_pkg() to facilitate
    testing R packages."""

    homepage = "https://cran.r-project.org/package=testit"
    url      = "https://cran.r-project.org/src/contrib/testit_0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/testit"

    version('0.7', 'cfc5f5c66aa644fbf53efc4b29d18e8c')
    version('0.5', 'f206d3cbdc5174e353d2d05ba6a12e59')
