# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPcapp(RPackage):
    """Provides functions for robust PCA by projection pursuit."""

    homepage = "https://cloud.r-project.org/package=pcaPP"
    url      = "https://cloud.r-project.org/src/contrib/pcaPP_1.9-72.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pcaPP"

    version('1.9-73', sha256='ca4566b0babfbe83ef9418283b08a12b3420dc362f93c6562f265df7926b53fc')
    version('1.9-72.1', sha256='a9e39ee15a650930c07672092f9f0c431807869b68b5471037eb7290a4d65bd5')
    version('1.9-72', '87c08f8ecab69311bba395c026bbc91c')
    version('1.9-70', '3fcc809ec1cdc910f10e9ebf372888e8')
    version('1.9-61', '1bd5bc3aff968b168493e8c523d726ea')
    version('1.9-60', '23dd468abb9fedc11e40166446df1017')
    version('1.9-50', 'be44f173404fd6e86ba0a5515711bfa3')

    depends_on('r-mvtnorm', type=('build', 'run'))
