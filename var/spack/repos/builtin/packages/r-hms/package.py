# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHms(RPackage):
    """Pretty Time of Day

    Implements an S3 class for storing and formatting time-of-day values, based
    on the 'difftime' class."""

    homepage = "https://cloud.r-project.org/package=hms"
    cran = "hms"

    version('1.1.1', sha256='6b5f30db1845c70d27b5de33f31caa487cdd0787cd80a4073375e5f482269062')
    version('1.0.0', sha256='9704e903d724f0911d46e5ad18b469a7ed419c5b1f388bd064fd663cefa6c962')
    version('0.5.0', sha256='a87872665c3bf3901f597d78c152e7805f7129e4dbe27397051de4cf1a76561b')
    version('0.3', sha256='9368259cbc1094ce0e4cf61544875ec30088ef690d6667e6b0b564218ab3ff88')

    depends_on('r-ellipsis', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-ellipsis@0.3.2', when='@1.1:', type=('build', 'run'))
    depends_on('r-lifecycle', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-pkgconfig', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.2.0:', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.2.1:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.3.8:', when='@1.1:', type=('build', 'run'))
