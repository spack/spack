# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPreprocesscore(RPackage):
    """A library of core preprocessing routines"""

    homepage = "https://bioconductor.org/packages/preprocessCore/"
    git      = "https://git.bioconductor.org/packages/preprocessCore.git"

    version('1.38.1', commit='c58cb4c720eda0f1c733b989b14912093a7c5fbc')
    version('1.44.0', branch='RELEASE_3_8')

    depends_on('r@3.4.0:3.4.9', when='@1.38.1')
