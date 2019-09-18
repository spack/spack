# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFlexmix(RPackage):
    """flexmix: Flexible Mixture Modeling"""

    homepage = "https://cloud.r-project.org/package=flexmix"
    url      = "https://cloud.r-project.org/src/contrib/flexmix_2.3-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/flexmix"

    version('2.3-15', sha256='ba444c0bfe33ab87d440ab590c06b03605710acd75811c1622253171bb123f43')
    version('2.3-14', '5be4f7764e6a697f4586e60c2bf6e960')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-modeltools@0.2-16:', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
