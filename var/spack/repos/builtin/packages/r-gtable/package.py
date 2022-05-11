# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RGtable(RPackage):
    """Arrange 'Grobs' in Tables.

    Tools to make it easier to work with "tables" of 'grobs'. The 'gtable'
    package defines a 'gtable' grob class that specifies a grid along with a
    list of grobs and their placement in the grid. Further the package makes it
    easy to manipulate and combine 'gtable' objects so that complex
    compositions can be build up sequentially."""

    cran = "gtable"

    version('0.3.0', sha256='fd386cc4610b1cc7627dac34dba8367f7efe114b968503027fb2e1265c67d6d3')
    version('0.2.0', sha256='801e4869830ff3da1d38e41f5a2296a54fc10a7419c6ffb108582850c701e76f')

    depends_on('r@3.0:', type=('build', 'run'))
