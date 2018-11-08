# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPhytools(RPackage):
    """Phylogenetic Tools for Comparative Biology (and Other Things)"""

    homepage = "http://github.com/liamrevell/phytools"
    url      = "https://cran.r-project.org/src/contrib/phytools_0.6-60.tar.gz"

    version('0.6-60', sha256='55cad759510d247ebbf03a53a46caddadd3bf87584ccf7fcd6dd06d44516b377')

    depends_on('r-animation', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-clustergeneration', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-combinat', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-phangorn', type=('build', 'run'))
    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
