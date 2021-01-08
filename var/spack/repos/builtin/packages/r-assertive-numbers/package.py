# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveNumbers(RPackage):
    """assertive.numbers: Assertions to Check Properties of Numbers"""

    homepage = "https://cloud.r-project.org/package=assertive.numbers"
    url      = "https://cloud.r-project.org/src/contrib/assertive.numbers_0.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.numbers"

    version('0.0-2', sha256='bae18c0b9e5b960a20636e127eb738ecd8a266e5fc29d8bc5ca712498cd68349')

    extends('r')
    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
