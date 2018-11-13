# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMakecdfenv(RPackage):
    """This package has two functions. One reads a Affymetrix
    chip description file (CDF) and creates a hash table environment
    containing the location/probe set membership mapping.
    The other creates a package that automatically loads
    that environment."""

    homepage = "https://www.bioconductor.org/packages/makecdfenv/"
    git      = "https://git.bioconductor.org/packages/makecdfenv.git"

    version('1.52.0', commit='b88a3e93e3b7feeeca69eda7c1fc5a0826c81120')

    depends_on('r@3.4.0:3.4.9', when='@1.52.0')
    depends_on('r-affyio', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
