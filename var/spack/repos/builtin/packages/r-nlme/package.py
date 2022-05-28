# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNlme(RPackage):
    """Linear and Nonlinear Mixed Effects Models.

    Fit and compare Gaussian linear and nonlinear mixed-effects models."""

    cran = "nlme"

    version('3.1-155', sha256='9f390f842852422921b5845130ea73c1f006d7bb5e988e82f728093a0cbdff4f')
    version('3.1-153', sha256='3d27a98edf1b16ee868949e823ac0babbf10c937a7220d648b7ef9480cd680e3')
    version('3.1-152', sha256='5b65d1b1f121caf29e60341acf6d85e267fd94ed517748cf42d36359f74e515e')
    version('3.1-151', sha256='a2c626bad68bf582663005170d1b9d844a10dca8efb13597f15ffb4b1fe886ca')
    version('3.1-141', sha256='910046260a03d8f776ac7b0766b5adee91556829d0d8a70165b2c695ce038056')
    version('3.1-139', sha256='0460fc69d85122177e7ef01bad665d56bcaf63d31bdbfdbdfdcba2c082085739')
    version('3.1-131', sha256='79daa167eb9bc7d8dba506da4b24b5250665b051d4e0a51dfccbb0087fdb564c')
    version('3.1-130', sha256='ec576bd906ef2e1c79b6a4382743d425846f63be2a43de1cce6aa397b40e290e')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.3.0:', type=('build', 'run'), when='@3.1-131.1')
    depends_on('r@3.5.0:', type=('build', 'run'), when='@3.1-134:3.1-135')
    depends_on('r@3.4.0:', type=('build', 'run'), when='@3.1-135.5:')
    depends_on('r-lattice', type=('build', 'run'))
