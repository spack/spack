# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNlme(RPackage):
    """Fit and compare Gaussian linear and nonlinear mixed-effects models."""

    homepage = "https://cloud.r-project.org/package=nlme"
    url      = "https://cloud.r-project.org/src/contrib/nlme_3.1-130.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nlme"

    version('3.1-141', sha256='910046260a03d8f776ac7b0766b5adee91556829d0d8a70165b2c695ce038056')
    version('3.1-139', sha256='0460fc69d85122177e7ef01bad665d56bcaf63d31bdbfdbdfdcba2c082085739')
    version('3.1-131', '0f1215ec4d4e3bca939282d122f4d1fa')
    version('3.1-130', '1935d6e308a8018ed8e45d25c8731288')
    version('3.1-128', '3d75ae7380bf123761b95a073eb55008')

    depends_on('r@3.0.2:', when='@:3.1-131', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@3.1-131.1', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@3.1-135.5:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@3.1-134:3.1-135', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
