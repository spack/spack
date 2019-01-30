# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RChron(RPackage):
    """Chronological objects which can handle dates and times."""

    homepage = "https://cran.r-project.org/package=chron"
    url      = "https://cran.r-project.org/src/contrib/chron_2.3-47.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/chron"

    version('2.3-47', 'b8890cdc5f2337f8fd775b0becdcdd1f')
