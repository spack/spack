# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GlobusToolkit(AutotoolsPackage):
    """The Globus Toolkit is an open source software toolkit used for building
       grids"""

    homepage = "http://toolkit.globus.org"
    url      = "http://toolkit.globus.org/ftppub/gt6/installers/src/globus_toolkit-6.0.1506371041.tar.gz"

    version('6.0.1506371041', 'e17146f68e03b3482aaea3874d4087a5')
    version('6.0.1493989444', '9e9298b61d045e65732e12c9727ceaa8')

    depends_on('pkgconfig', type='build')
    depends_on('openssl')
