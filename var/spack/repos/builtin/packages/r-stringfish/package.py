# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RStringfish(RPackage):
    """Alt String Implementation.

    Provides an extendable, performant and multithreaded 'alt-string'
    implementation backed by 'C++' vectors and strings."""

    cran = "stringfish"

    maintainers = ['dorton21']

    version('0.15.5', sha256='9df21146a7710e5a9ab4bb53ebc231a580c798b7e541b8d78df53207283f8129')
    version('0.14.2', sha256='9373cfc715cda1527fd20179435977b8e59e19d8c5ef82a31e519f93fb624ced')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r@3.0.2:', type=('build', 'run'), when='@0.15.5:')
    depends_on('r-rcpp@0.12.18.3:', type=('build', 'run'))
    depends_on('r-rcppparallel', type=('build', 'run'))
    depends_on('gmake', type='build')
