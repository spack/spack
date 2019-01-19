# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRandomfields(RPackage):
    """Methods for the inference on and the simulation of Gaussian fields
       are provided, as well as methods for the simulation of extreme
       value random fields."""

    homepage = "https://cran.r-project.org/web/packages/RandomFields"
    url = "https://cran.r-project.org/src/contrib/RandomFields_3.1.50.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RandomFields"

    version('3.1.50', 'fd91aea76365427c0ba3b25fb3af43a6')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-randomfieldsutils@0.3.25:', type=('build', 'run'))
