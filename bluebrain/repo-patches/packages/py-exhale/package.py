# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyExhale(PythonPackage):
    """Automatic C++ library API documentation generator using Doxygen, Sphinx, and Breathe.
    Exhale revives Doxygen's class / file hierarchies using reStructuredText
    for superior markup syntax / websites.
    """

    homepage = "https://github.com/svenevs/exhale"
    url      = "https://pypi.org/packages/source/e/exhale/exhale-0.2.2.tar.gz"

    version('develop', git=url, branch='master', get_full_repo=True)
    version('0.2.2', sha256='16f8ca9c63fd35eb1c7d4b52e182b04f3275ec6cc3176d89e5b5d0a37bb0fe63')

    depends_on('py-setuptools', type='build')
    depends_on('py-beautifulsoup4', type=('build', 'run'))
    depends_on('py-breathe', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-sphinx', type=('build', 'run'))

    patch('py3-read-utf-8.diff', when='^python@3:')

    def patch(self):
        filter_file(r'^bs4', 'beautifulsoup4', 'requirements.txt')
