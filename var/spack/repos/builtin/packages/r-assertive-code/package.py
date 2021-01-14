# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveCode(RPackage):
    """assertive.code: Assertions to Check Properties of Code"""

    homepage = "https://cloud.r-project.org/package=assertive.code"
    url      = "https://cloud.r-project.org/src/contrib/assertive.code_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.code"

    version('0.0-3', sha256='ef80e8d1d683d776a7618e78ddccffca7f72ab4a0fcead90c670bb8f8cb90be2')

    extends('r')
    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2', type=('build', 'run'))
    depends_on('r-assertive-properties', type=('build', 'run'))
    depends_on('r-assertive-types', type=('build', 'run'))
