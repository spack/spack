# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMda(RPackage):
    """Mixture and flexible discriminant analysis, multivariate adaptive
    regression splines (MARS), BRUTO."""

    homepage = "https://cloud.r-project.org/package=mda"
    url      = "https://cloud.r-project.org/src/contrib/mda_0.4-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mda"

    version('0.4-10', sha256='7036bc622a8fea5b2de94fc19e6b64f5f0c27e5d743ae7646e116af08c9de6a5')
    version('0.4-9', '2ce1446c4a013e0ebcc1099a00269ad9')

    depends_on('r@1.9.0:', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
