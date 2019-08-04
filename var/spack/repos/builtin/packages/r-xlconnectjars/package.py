# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXlconnectjars(RPackage):
    """Provides external JAR dependencies for the XLConnect package."""

    homepage = "http://miraisolutions.wordpress.com/"
    url      = "https://cloud.r-project.org/src/contrib/XLConnectJars_0.2-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/XLConnectJars"

    version('0.2-15', sha256='bd6f48a72c3a02b7a5e9373bcfc671614bc793f41d7bb8f4f34115a89ff4f8c6')
    version('0.2-14', sha256='c675f0ccff0c3e56b2b1cc00d4d28bf8fdfa508266ac0ffab5c0641151dd7332')
    version('0.2-12', '6984e5140cd1c887c017ef6f88cbba81')
    version('0.2-9', 'e6d6b1acfede26acaa616ee421bd30fb')

    depends_on('r-rjava', type=('build', 'run'))
