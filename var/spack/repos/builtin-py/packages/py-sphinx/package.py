##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
    # TODO: incorporate the proper dependencies when concretizer is capable
    # Build dep for 1.6.1 all python (bug), see:
    # https://github.com/sphinx-doc/sphinx/pull/3789
    # depends_on('py-typing', when='@1.6.1', type=('build', 'run'))
    # depends_on('py-typing', when='@1.6.2:^python@2.7:3.4',
    #            type=('build', 'run'))
    depends_on('py-typing', when='@1.6:', type=('build', 'run'))

    depends_on('py-pytest',     type='test')
    depends_on('py-mock',       type='test')
    depends_on('py-simplejson', type='test')
    depends_on('py-html5lib',   type='test')
