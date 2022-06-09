# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Librttopo(AutotoolsPackage):
    """
    The RT Topology Library exposes an API to create and manage standard \
    (ISO 13249 aka SQL/MM) topologies using user-provided data stores.
    """

    homepage = "https://git.osgeo.org/gitea/rttopo"
    git      = "https://git.osgeo.org/gitea/rttopo/librttopo.git"

    version('1.1.0', tag='librttopo-1.1.0')

    depends_on('geos')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
