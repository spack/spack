# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RTestit(RPackage):
    """Provides two convenience functions assert() and test_pkg() to facilitate
    testing R packages."""

    homepage = "https://cloud.r-project.org/package=testit"
    url      = "https://cloud.r-project.org/src/contrib/testit_0.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/testit"

    version('0.9', sha256='9cf6b3df9b2c700e4e7dcbd5b8cb64fabefe674e1f40346ccaf39fe7feda5e55')
    version('0.8', sha256='08a9c19c962eae60f4ab58885a23e0bc239efc39da682290be436c066f8d97f7')
    version('0.7', 'cfc5f5c66aa644fbf53efc4b29d18e8c')
    version('0.5', 'f206d3cbdc5174e353d2d05ba6a12e59')
