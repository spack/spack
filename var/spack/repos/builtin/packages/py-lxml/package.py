# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLxml(PythonPackage):
    """lxml is the most feature-rich and easy-to-use library for processing
    XML and HTML in the Python language."""

    homepage = "http://lxml.de/"
    url      = "https://pypi.io/packages/source/l/lxml/lxml-4.4.1.tar.gz"

    version('4.4.1', sha256='c81cb40bff373ab7a7446d6bbca0190bccc5be3448b47b51d729e37799bb5692')
    version('4.3.3', sha256='4a03dd682f8e35a10234904e0b9508d705ff98cf962c5851ed052e9340df3d90')
    version('4.2.5', sha256='36720698c29e7a9626a0dc802ef8885f8f0239bfd1689628ecd459a061f2807f')
    version('3.7.3', sha256='aa502d78a51ee7d127b4824ff96500f0181d3c7826e6ee7b800d068be79361c7')
    version('2.3', sha256='eea1b8d29532739c1383cb4794c5eacd6176f0972b59e8d29348335b87ff2e66')

    variant('html5', default=False, description='Enable html5lib backend')
    variant('htmlsoup',  default=False, description='Enable BeautifulSoup4 backend')
    variant('cssselect',   default=False, description='Enable cssselect module')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('libxml2', type=('build', 'run'))
    depends_on('libxslt', type=('build', 'run'))
    depends_on('py-html5lib', when='+html5', type=('build', 'run'))
    depends_on('py-beautifulsoup4', when='+htmlsoup', type=('build', 'run'))
    depends_on('py-cssselect@0.7:', when='+cssselect', type=('build', 'run'))
