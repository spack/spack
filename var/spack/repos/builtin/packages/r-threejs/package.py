# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RThreejs(RPackage):
    """Create interactive 3D scatter plots, network plots, and globes using the
    'three.js' visualization library ("http://threejs.org")."""

    homepage = "http://bwlewis.github.io/rthreejs"
    url      = "https://cloud.r-project.org/src/contrib/threejs_0.2.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/threejs"

    version('0.2.2', '35c179b10813c5e4bd3e7827fae6627b')

    depends_on('r-htmlwidgets@0.3.2:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-igraph@1.0.0:', when='@0.3.1:', type=('build', 'run'))
    depends_on('r-crosstalk', when='@0.3.1:', type=('build', 'run'))
