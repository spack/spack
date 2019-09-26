# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStringr(RPackage):
    """A consistent, simple and easy to use set of wrappers around the
    fantastic 'stringi' package. All function and argument names (and
    positions) are consistent, all functions deal with "NA"'s and zero length
    vectors in the same way, and the output from one function is easy to feed
    into the input of another."""

    homepage = "https://cloud.r-project.org/package=stringr"
    url      = "https://cloud.r-project.org/src/contrib/stringr_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/stringr"

    version('1.4.0', sha256='87604d2d3a9ad8fd68444ce0865b59e2ffbdb548a38d6634796bbd83eeb931dd')
    version('1.3.1', sha256='7a8b8ea038e45978bd797419b16793f44f10c5355ad4c64b74d15276fef20343')
    version('1.2.0', '9054b1de91c578cc5cf454d656e9c697')
    version('1.1.0', '47973a33944c6d5db9524b1e835b8a5d')
    version('1.0.0', '5ca977c90351f78b1b888b379114a7b4')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-stringi@1.1.7:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-glue@1.2.0:', when='@1.3.0:', type=('build', 'run'))
