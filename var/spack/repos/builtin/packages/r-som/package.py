# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSom(RPackage):
    """Self-Organizing Map (with application in gene clustering)."""

    homepage = "https://cloud.r-project.org/package=som"
    url      = "https://cloud.r-project.org/src/contrib/som_0.3-5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/som"

    version('0.3-5.1', '802a5a80902579354ce3420faeeeb756')
    version('0.3-5', '72717499794c7aa945a768b742af8895')
    version('0.3-4', '1e25572e446409f5e32c5da5f1af98e6')
    version('0.3-3', 'd4ac444be24f71d08b99974c2f4b96e5')
    version('0.3-2', '4ce28f46df68fbb73905711ba2416fac')

    depends_on('r@2.10:', type=('build', 'run'))
