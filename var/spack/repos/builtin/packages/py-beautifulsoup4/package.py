# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeautifulsoup4(PythonPackage):
    """Beautiful Soup is a Python library for pulling data out of HTML and
    XML files. It works with your favorite parser to provide idiomatic ways
    of navigating, searching, and modifying the parse tree."""

    homepage = "https://www.crummy.com/software/BeautifulSoup"
    pypi = "beautifulsoup4/beautifulsoup4-4.8.0.tar.gz"

    version('4.9.3', sha256='84729e322ad1d5b4d25f805bfa05b902dd96450f43842c4e99067d5e1369eb25')
    version('4.8.0', sha256='25288c9e176f354bf277c0a10aa96c782a6a18a17122dba2e8cec4a97e03343b')
    version('4.5.3', sha256='b21ca09366fa596043578fd4188b052b46634d22059e68dd0077d9ee77e08a3e')
    version('4.5.1', sha256='3c9474036afda9136aac6463def733f81017bf9ef3510d25634f335b0c87f5e1')
    version('4.4.1', sha256='87d4013d0625d4789a4f56b8d79a04d5ce6db1152bb65f1d39744f7709a366b4')

    variant('lxml', default=False, description='Enable lxml parser')
    variant('html5lib', default=False, description='Enable html5lib parser')

    depends_on('py-setuptools', type='build')
    depends_on('py-soupsieve@1.3:', when='@4.9.0: ^python@3:', type=('build', 'run'))
    depends_on('py-soupsieve@1.3:1.99', when='@4.9.0: ^python@:2.8', type=('build', 'run'))
    depends_on('py-soupsieve@1.2:', when='@4.7.0:', type=('build', 'run'))

    depends_on('py-lxml', when='+lxml', type=('build', 'run'))
    depends_on('py-html5lib', when='+html5lib', type=('build', 'run'))
