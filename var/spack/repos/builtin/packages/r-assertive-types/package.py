# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveTypes(RPackage):
    """assertive.types: Assertions to Check Types of Variables"""

    homepage = "https://cloud.r-project.org/package=assertive.types"
    url      = "https://cloud.r-project.org/src/contrib/assertive.types_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.types"

    version('0.0-3', sha256='ab6db2eb926e7bc885f2043fab679330aa336d07755375282d89bf9f9d0cb87f')

    depends_on('r-assertive-base@0.0-7:', type=('build', 'run'))
    depends_on('r-assertive-properties', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
