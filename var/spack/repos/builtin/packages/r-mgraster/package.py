# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMgraster(RPackage):
    """Convenience Functions for R Language Access to the v.1 API of the
    MG-RAST Metagenome Annotation Server, part of the US Department of Energy
    (DOE) Systems Biology Knowledge Base (KBase)."""

    homepage = "https://github.com/braithwaite/MGRASTer/"
    url      = "https://cloud.r-project.org/src/contrib/MGRASTer_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MGRASTer"

    version('0.9', '902c7ad4180b858d6b6428ea26d7652a')

    depends_on('r@3:', type=('build', 'run'))
