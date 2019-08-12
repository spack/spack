# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTimedate(RPackage):
    """Environment for teaching "Financial Engineering and Computational
    Finance". Managing chronological and calendar objects."""

    homepage = "https://cran.r-project.org/package=timeDate"
    url      = "https://cran.r-project.org/src/contrib/timeDate_3012.100.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/timeDate"

    version('3012.100', '9f69d3724efbf0e125e6b8e6d3475fe4')
