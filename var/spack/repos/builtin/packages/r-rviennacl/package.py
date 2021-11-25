# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRviennacl(RPackage):
    """RViennaCL: 'ViennaCL' C++ Header Files"""

    homepage = "https://cloud.r-project.org/package=RViennaCL"
    url      = "https://cloud.r-project.org/src/contrib/RViennaCL_1.7.1.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RViennaCL"

    version('1.7.1.8', sha256='adcc74537337582153d5b11d281e391e91a7f3afae116aa1b9a034ffd11b0252')
