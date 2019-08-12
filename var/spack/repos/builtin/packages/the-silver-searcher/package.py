# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TheSilverSearcher(AutotoolsPackage):
    """Fast recursive grep alternative"""

    homepage = "http://geoff.greer.fm/ag/"
    url      = "http://geoff.greer.fm/ag/releases/the_silver_searcher-0.32.0.tar.gz"

    version('2.1.0', '3e7207b060424174323236932bf76ec2')
    version('0.32.0', '3fdfd5836924246073d5344257a06823')
    version('0.30.0', '95e2e7859fab1156c835aff7413481db')

    depends_on('pcre')
    depends_on('xz')
    depends_on('zlib')
    depends_on('pkgconfig', type='build')
