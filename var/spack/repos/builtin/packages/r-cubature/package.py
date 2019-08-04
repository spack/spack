# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCubature(RPackage):
    """Adaptive multivariate integration over hypercubes"""

    homepage = "https://cloud.r-project.org/package=cubature"
    url      = "https://cloud.r-project.org/src/contrib/cubature_1.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cubature"

    version('2.0.3', sha256='79bf03ebdb64b0de1ef19d24051b9d922df9310254bee459bb47764522407a73')
    version('2.0.2', sha256='641165c665ff490c523bccc05c42bb6851e42676b6b366b55fc442a51a8fbe8c')
    version('1.1-2', '5617e1d82baa803a3814d92461da45c9')

    depends_on('r-rcpp', when='@2.0.3:', type=('build', 'run'))
