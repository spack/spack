# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXlconnectjars(RPackage):
    """Provides external JAR dependencies for the XLConnect package."""

    homepage = "http://miraisolutions.wordpress.com/"
    url      = "https://cran.r-project.org/src/contrib/XLConnectJars_0.2-9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/XLConnectJars"

    version('0.2-12', '6984e5140cd1c887c017ef6f88cbba81')
    version('0.2-9', 'e6d6b1acfede26acaa616ee421bd30fb')

    depends_on('r-rjava', type=('build', 'run'))
