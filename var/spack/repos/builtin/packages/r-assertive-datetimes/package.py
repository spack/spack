# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveDatetimes(RPackage):
    """assertive.datetimes: Assertions to Check Properties of Dates and Times"""

    homepage = "https://cloud.r-project.org/package=assertive.datetimes"
    url      = "https://cloud.r-project.org/src/contrib/assertive.datetimes_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.datetimes"

    version('0.0-3', sha256='014e2162f5a8d95138ed8330f7477e71c908a29341697c09a1b7198b7e012d94')

    extends('r')
    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base', type=('build', 'run'))
    depends_on('r-assertive-types', type=('build', 'run'))
