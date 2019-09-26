# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGss(RPackage):
    """A comprehensive package for structural multivariate function
    estimation using smoothing splines."""

    homepage = "https://cloud.r-project.org/package=gss"
    url      = "https://cloud.r-project.org/src/contrib/gss_2.1-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gss"

    version('2.1-10', sha256='26c47ecae6a9b7854a1b531c09f869cf8b813462bd8093e3618e1091ace61ee2')
    version('2.1-7', '4a6bd96339d22b40c932895b64504fb2')

    depends_on('r@2.14.0:', type=('build', 'run'))
