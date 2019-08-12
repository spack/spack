# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAmap(RPackage):
    """Tools for Clustering and Principal Component Analysis
       (With robust methods, and parallelized functions)."""

    homepage = "http://mulcyber.toulouse.inra.fr/projects/amap/"
    url      = "https://cran.rstudio.com/src/contrib/amap_0.8-16.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/amap/"

    version('0.8-16', sha256='d3775ad7f660581f7d2f070e426be95ae0d6743622943e6f5491988e5217d4e2')

    depends_on('r@2.10.0:', type=('build', 'run'))
