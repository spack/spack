# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REnergy(RPackage):
    """E-Statistics: Multivariate Inference via the Energy of Data"""

    homepage = "https://cloud.r-project.org/web/packages/energy/index.html"
    url      = "https://cloud.r-project.org/src/contrib/energy_1.7-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/energy"

    version('1.7-6', sha256='900edbb28e1f1bccd78580828470628cf75eb6333b63e1a58e4da7fc5c5fa89a')
    version('1.7-5', 'd13c76c26b5221ba29aade6a824f32d6')

    depends_on('r-rcpp@0.12.6:', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
