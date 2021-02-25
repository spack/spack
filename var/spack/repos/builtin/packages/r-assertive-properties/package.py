# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveProperties(RPackage):
    """assertive.properties: Assertions to Check Properties of Variables"""

    homepage = "https://cloud.r-project.org/package=assertive.properties"
    url      = "https://cloud.r-project.org/src/contrib/assertive.properties_0.0-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.properties"

    version('0.0-4', sha256='5c0663fecb4b7c30f2e1d65da8644534fcfe97fb3d8b51f74c1327cd14291a6b')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-7:', type=('build', 'run'))
