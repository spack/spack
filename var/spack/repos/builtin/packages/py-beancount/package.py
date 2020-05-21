# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeancount(PythonPackage):
    """A double-entry bookkeeping computer language that lets you define
       financial transaction records in a text file, read them in memory, 
       generate a variety of reports from them, and provides a web 
       interface.."""

    homepage = "http://furius.ca/beancount/"
    url      = "https://pypi.io/packages/source/b/beancount/beancount-2.2.3.tar.gz"
    hg       = "https://bitbucket.org/blais/beancount/"

    version('master', revision='default')
    version('2.2.3',  sha256='1554adfd773d12cb88fd7f4da67fcb608665a9bdedc7e44834e059d1b3a08e5d')

    depends_on('mercurial',          type=('build'))
    depends_on('python@3.5:',        type=('build', 'run'))
    depends_on('py-setuptools',      type=('build'))
    depends_on('py-pytest',          type=('test', 'run'))

    depends_on('py-bottle',          type=('build', 'run'))
    depends_on('py-lxml+htmlsoup',   type=('build', 'run'))
    depends_on('py-ply',             type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-magic',    type=('build', 'run'))
    depends_on('py-beautifulsoup4',  type=('build', 'run'))
    depends_on('py-requests',        type=('build', 'run'))
    depends_on('py-chardet',         type=('build', 'run'))
    depends_on('py-google-api-python-client', type=('build', 'run'))
