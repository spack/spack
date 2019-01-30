# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGmodels(RPackage):
    """Various R programming tools for model fitting."""

    homepage = "http://www.sf.net/projects/r-gregmisc"
    url      = "https://cran.r-project.org/src/contrib/gmodels_2.16.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gmodels"

    version('2.16.2', 'f13e5feb2a8b9f0cd47fdf25ddc74228')

    depends_on('r@1.9:')
    depends_on('r-gdata', type=('build', 'run'))
