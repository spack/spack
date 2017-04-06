##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    url      = "https://pypi.io/packages/source/S/Sphinx/Sphinx-1.5.5.tar.gz"

    version('1.5.5', 'f9581b3556df9722143c47290273bcf8')
    version('1.4.5', '5c2cd2dac45dfa6123d067e32a89e89a')
    version('1.3.1', '8786a194acf9673464c5455b11fd4332')

    extends('python', ignore='bin/(pybabel|pygmentize)')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-sphinx requires py-setuptools during runtime as well.
    depends_on('py-setuptools',              type=('build', 'run'))

    depends_on('py-six@1.4:',                type=('build', 'run'))
    depends_on('py-jinja2@2.3:',             type=('build', 'run'))
    depends_on('py-pygments@2.0:',           type=('build', 'run'))
    depends_on('py-docutils@0.11:',          type=('build', 'run'))
    depends_on('py-snowballstemmer@1.1:',    type=('build', 'run'))
    depends_on('py-babel@1.3:',              type=('build', 'run'))  # not 2.0
    depends_on('py-alabaster@0.7:',          type=('build', 'run'))
    depends_on('py-imagesize', when='@1.4:', type=('build', 'run'))
    depends_on('py-sphinx-rtd-theme@0.1:',   type=('build', 'run'))  # optional as of 1.4
