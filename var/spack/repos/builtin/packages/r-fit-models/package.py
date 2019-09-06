# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFitModels(RPackage):
    """Compare Fitted Models"""

    homepage = "https://cloud.r-project.org/package=fit.models"
    url      = "https://cloud.r-project.org/src/contrib/fit.models_0.5-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fit.models"

    version('0.5-14', '159b5c57953db4c917bc186ddacdff51')
    version('0.5-13', 'c9ff87e98189bcc3be597e3833408497')

    depends_on('r-lattice', type=('build', 'run'))
