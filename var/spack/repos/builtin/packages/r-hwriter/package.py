# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHwriter(RPackage):
    """Easy-to-use and versatile functions to
    output R objects in HTML format."""

    homepage = "https://cloud.r-project.org/package=hwriter"
    url      = "https://cloud.r-project.org/src/contrib/hwriter_1.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/hwriter"

    version('1.3.2', '9eef49df2eb68bbf3a16b5860d933517')

    depends_on('r@2.6.0:', type=('build', 'run'))
