# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RThreejs(RPackage):
    """Create interactive 3D scatter plots, network plots, and globes using the
    'three.js' visualization library ("http://threejs.org")."""

    homepage = "http://bwlewis.github.io/rthreejs"
    url      = "https://cran.r-project.org/src/contrib/threejs_0.2.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/threejs"
    version('0.2.2', '35c179b10813c5e4bd3e7827fae6627b')

    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
