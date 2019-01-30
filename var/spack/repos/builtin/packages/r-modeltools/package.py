# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RModeltools(RPackage):
    """A collection of tools to deal with statistical models."""

    homepage = "https://cran.r-project.org/package=modeltools"
    url      = "https://cran.r-project.org/src/contrib/modeltools_0.2-21.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/modeltools"

    version('0.2-21', '3bf56b2e7bf78981444385d87eeccdd7')
