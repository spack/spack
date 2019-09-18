# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeautifulsoup4(PythonPackage):
    """Beautiful Soup is a Python library for pulling data out of HTML and
    XML files. It works with your favorite parser to provide idiomatic ways
    of navigating, searching, and modifying the parse tree."""

    homepage = "https://www.crummy.com/software/BeautifulSoup"
    url = "https://pypi.io/packages/source/b/beautifulsoup4/beautifulsoup4-4.8.0.tar.gz"

    version('4.8.0', sha256='25288c9e176f354bf277c0a10aa96c782a6a18a17122dba2e8cec4a97e03343b')
    version('4.5.3', '937e0df0d699a1237646f38fd567f0c6')
    version('4.5.1', '994abd90e691beaf7d42c00ffb2f3a67')
    version('4.4.1', '8fbd9a7cac0704645fa20d1419036815')

    depends_on('py-setuptools', type='build')
    depends_on('py-soupsieve@1.2:', when='@4.7.0:', type=('build', 'run'))
