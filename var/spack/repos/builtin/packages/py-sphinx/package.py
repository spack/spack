# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinx(PythonPackage):
    """Sphinx Documentation Generator."""
    homepage = "http://sphinx-doc.org"
    url      = "https://pypi.io/packages/source/S/Sphinx/Sphinx-1.6.1.tar.gz"

    import_modules = [
        'sphinx', 'sphinx.testing', 'sphinx.ext', 'sphinx.pycode',
        'sphinx.search', 'sphinx.transforms', 'sphinx.builders',
        'sphinx.directives', 'sphinx.util', 'sphinx.environment',
        'sphinx.writers', 'sphinx.domains', 'sphinx.locale',
        'sphinx.ext.napoleon', 'sphinx.ext.autosummary', 'sphinx.pycode.pgen2',
        'sphinx.transforms.post_transforms', 'sphinx.util.stemmer',
        'sphinx.environment.collectors', 'sphinx.environment.adapters'
    ]

    version('1.8.4',   sha256='c1c00fc4f6e8b101a0d037065043460dffc2d507257f2f11acaed71fd2b0c83c')
    version('1.8.2',   sha256='120732cbddb1b2364471c3d9f8bfd4b0c5b550862f99a65736c77f970b142aea')
    version('1.7.4', sha256='e9b1a75a3eae05dded19c80eb17325be675e0698975baae976df603b6ed1eb10')
    version('1.6.3', sha256='af8bdb8c714552b77d01d4536e3d6d2879d6cb9d25423d29163d5788e27046e6')
    version('1.6.1', sha256='7581d82c3f206f0ac380edeeba890a2e2d2be011e5abe94684ceb0df4b6acc3f')
    version('1.5.5', sha256='4064ea6c56feeb268838cb8fbbee507d0c3d5d92fa63a7df935a916b52c9e2f5')
    version('1.4.5', sha256='c5df65d97a58365cbf4ea10212186a9a45d89c61ed2c071de6090cdf9ddb4028')
    version('1.3.1', sha256='1a6e5130c2b42d2de301693c299f78cc4bd3501e78b610c08e45efc70e2b5114')

    extends('python', ignore='bin/(pybabel|pygmentize)')

    # Sphinx requires at least Python 2.7 or 3.4 to run
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    # See here for upstream list of dependencies:
    # https://github.com/sphinx-doc/sphinx/blob/master/setup.py

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-sphinx requires py-setuptools during runtime as well.
    depends_on('py-setuptools',               type=('build', 'run'))

    depends_on('py-six@1.5:',                 type=('build', 'run'))
    depends_on('py-jinja2@2.3:',              type=('build', 'run'))
    depends_on('py-pygments@2.0:',            type=('build', 'run'))
    depends_on('py-docutils@0.11:',           type=('build', 'run'))
    depends_on('py-snowballstemmer@1.1:',     type=('build', 'run'))
    depends_on('py-babel@1.3:',               type=('build', 'run'))  # not 2.0
    depends_on('py-alabaster@0.7.0:0.7.999',  type=('build', 'run'))
    depends_on('py-imagesize', when='@1.4:',  type=('build', 'run'))
    depends_on('py-requests@2.0.0:',          type=('build', 'run'))
    depends_on('py-sphinx-rtd-theme@0.1:',    type=('build', 'run'))  # optional as of 1.4
    # See: https://github.com/sphinx-doc/sphinx/commit/854a227501a7582510eba41a208d25816f754e0c
    depends_on('py-packaging', type=('build', 'run'), when='@1.7.4:')

    # Sphinx v1.6+ no longer includes websupport by default:
    # http://www.sphinx-doc.org/en/stable/changes.html
    depends_on('py-sphinxcontrib-websupport', when='@1.6:',
               type=('build', 'run'))
    # Build dep for 1.6.1 all python (bug), see:
    # https://github.com/sphinx-doc/sphinx/pull/3789
    depends_on('py-typing', when='@1.6.1', type=('build', 'run'))
    depends_on('py-typing', when='@1.6.2:^python@2.7:3.4', type=('build', 'run'))

    depends_on('py-pytest',     type='test')
    depends_on('py-mock',       type='test')
    depends_on('py-simplejson', type='test')
    depends_on('py-html5lib',   type='test')
