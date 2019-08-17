# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGtable(RPackage):
    """Tools to make it easier to work with "tables" of 'grobs'."""

    homepage = "https://cloud.r-project.org/package=gtable"
    url      = "https://cloud.r-project.org/src/contrib/gtable_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gtable"

    version('0.3.0', sha256='fd386cc4610b1cc7627dac34dba8367f7efe114b968503027fb2e1265c67d6d3')
    version('0.2.0', '124090ae40b2dd3170ae11180e0d4cab')

    depends_on('r@3.0:', type=('build', 'run'))
