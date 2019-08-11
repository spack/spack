# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMemoise(RPackage):
    """Cache the results of a function so that when you call it again with the
    same arguments it returns the pre-computed value."""

    homepage = "https://github.com/hadley/memoise"
    url      = "https://cloud.r-project.org/src/contrib/memoise_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/memoise"
    version('1.1.0', '493209ee04673f0fcab473c3dd80fb8c')
    version('1.0.0', 'd31145292e2a88ae9a504cab1602e4ac')

    depends_on('r-digest@0.6.3:', type=('build', 'run'))
