# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RModelr(RPackage):
    """Functions for modelling that help you seamlessly integrate modelling
       into a pipeline of data manipulation and visualisation."""

    homepage = "https://github.com/hadley/modelr"
    url      = "https://cloud.r-project.org/src/contrib/modelr_0.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/modelr"

    version('0.1.5', sha256='45bbee387c6ba154f9f8642e9f03ea333cce0863c324ff15d23096f33f85ce5a')
    version('0.1.4', sha256='b4da77c1244bbda512ce323751c8338741eeaa195283f172a0feec2917bcfdd9')
    version('0.1.3', sha256='e536b247c17d6cacf10565dd8a1b744efc90a8815c70edd54371e413e6d1b423')
    version('0.1.1', 'ce5fd088fb7850228ab1e34d241a975d')

    depends_on('r@3.1:', when='@:0.1.4', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.1.5:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-purrr@0.2.2:', type=('build', 'run'))
    depends_on('r-lazyeval@0.2.0:', when='@:0.1.1', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-broom', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr@0.8.0:', type=('build', 'run'))
    depends_on('r-rlang@0.2.0:', when='@0.1.3:', type=('build', 'run'))
