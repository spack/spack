# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinx(PythonPackage):
    """Sphinx Documentation Generator."""
    homepage = "http://sphinx-doc.org"
    url      = "https://github.com/sphinx-doc/sphinx/archive/v1.8.2.tar.gz"

    import_modules = [
        'sphinx', 'sphinx.testing', 'sphinx.ext', 'sphinx.pycode',
        'sphinx.search', 'sphinx.transforms', 'sphinx.builders',
        'sphinx.directives', 'sphinx.util', 'sphinx.environment',
        'sphinx.writers', 'sphinx.domains', 'sphinx.locale',
        'sphinx.ext.napoleon', 'sphinx.ext.autosummary', 'sphinx.pycode.pgen2',
        'sphinx.transforms.post_transforms', 'sphinx.util.stemmer',
        'sphinx.environment.collectors', 'sphinx.environment.adapters'
    ]

    version('1.8.2',   sha256='ee8fc3eadd4b13e8af77a38028c521e0f0fabe1e9e6eeab1a779e4f54329da22')
    version('1.8.1',   sha256='3ca0ff96399444078bef0185f45a8a587d0b306d1348a1b071c838d846a3c25d')
    version('1.8.0b1', sha256='c41fab93251d1b87f7087baad1575627ef395b5b51e6c3dde7fd79b91cf2722f')
    version('1.8.0',   sha256='7fa7e460ffcd4d276012dda5a662c4ce6c46454435c010c7382f3e6a4f16509f')
    version('1.7.9',   sha256='4c4777383f0f53a7689fa1d24155e90088fc111c0f45993f8d98b0e8b9e60236')
    version('1.7.8',   sha256='bffee8f401e7f239e3b82822f9279143545f3c4f9c9f0c7ffae001002419fcef')
    version('1.7.7',   sha256='bcad5233d8800d209cefec8d8b0279f7f4648d1fb90fddd32c166ad75ade3b9e')
    version('1.7.6',   sha256='7c3bce7ff32eb6142f918512fce48f8b1b209e668b9a5dbbefbb01cc2bb9288a')
    version('1.7.5',   sha256='2e93f4330dc44fc07d31e0de5d4f81e9281a78739208792fd08619b65c81c853')
    version('1.7.4', '95f3b83f521314600e5b09e99cf32c46')
    version('1.6.3', 'c5ad61f4e0974375ca2c2b58ef8d5411')
    version('1.6.1', '26cb1cdca7aa4afc8c925d926b6268e7')
    version('1.5.5', 'f9581b3556df9722143c47290273bcf8')
    version('1.4.5', '5c2cd2dac45dfa6123d067e32a89e89a')
    version('1.3.1', '8786a194acf9673464c5455b11fd4332')

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
