# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDryscrape(PythonPackage):
    """a lightweight Javascript-aware, headless web scraping library
       for Python"""

    homepage = "https://github.com/niklasb/dryscrape"
    url      = "https://pypi.io/packages/source/d/dryscrape/dryscrape-1.0.tar.gz"
    git      = "https://github.com/niklasb/dryscrape.git"

    version('develop', branch='master')
    version('1.0', '267e380a8efaf9cd8fd94de1639d3198')

    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-webkit-server@1.0:', type=('build', 'run'))
    depends_on('py-xvfbwrapper', type=('build', 'run'))
