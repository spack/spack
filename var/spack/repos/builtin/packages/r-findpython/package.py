# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFindpython(RPackage):
    """Package designed to find an acceptable python binary."""

    homepage = "https://github.com/trevorld/findpython"
    url      = "https://cran.r-project.org/src/contrib/findpython_1.0.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/findpython"

    version('1.0.3', sha256='5486535ae2f0a123b630d8eabf93a61b730765f55dfcc8ef4f6e56e7c49408f8')

    depends_on('python', type='run')
