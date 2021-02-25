# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveData(RPackage):
    """assertive.data: Assertions to Check Properties of Data"""

    homepage = "https://cloud.r-project.org/package=assertive.data"
    url      = "https://cloud.r-project.org/src/contrib/assertive.data_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.data"

    version('0.0-3', sha256='5a00fb48ad870d9b3c872ce3d6aa20a7948687a980f49fe945b455339e789b01')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
    depends_on('r-assertive-strings', type=('build', 'run'))
