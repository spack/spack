# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSm(RPackage):
    """This is software linked to the book 'Applied Smoothing Techniques for
       Data Analysis - The Kernel Approach with S-Plus Illustrations'
       Oxford University Press."""

    homepage = "http://www.stats.gla.ac.uk/~adrian/sm"
    url      = "https://cran.r-project.org/src/contrib/sm_2.2-5.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sm"

    version('2.2-5.5', sha256='43e212a14c364b98b10018b56fe0a619ccffe4bde1294e6c45b3eafe7caf82e7')

    depends_on('r@3.1.0:', type=('build', 'run'))
