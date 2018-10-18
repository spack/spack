# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiomUtils(RPackage):
    """Provides utilities to facilitate import, export and computation with
    the BIOM (Biological Observation Matrix) format (http://biom-format.org).
    """

    homepage = "https://github.com/braithwaite/BIOM.utils/"
    url      = "https://cran.r-project.org/src/contrib/BIOM.utils_0.9.tar.gz"

    version('0.9', '980f08fd9848242007753cd27a998060')

    depends_on('r@3:', type=('build', 'run'))
