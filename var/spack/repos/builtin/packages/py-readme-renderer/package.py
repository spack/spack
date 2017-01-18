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


class PyReadmeRenderer(PythonPackage):
    """readme_renderer is a library for rendering "readme" descriptions
    for Warehouse."""

    homepage = "https://github.com/pypa/readme_renderer"
    url      = "https://pypi.python.org/packages/f2/6e/ef1bc3a24eb14e14574aba9dc1bd50bc9a5e7cc880e8ff9cadd385b4fb37/readme_renderer-16.0.tar.gz"

    version('16.0', '70321cea986956bcf2deef9981569f39')

    depends_on('python@2.6:2.7,3.2:3.3')
    depends_on('py-setuptools', type='build')
    depends_on('py-bleach', type=('build', 'run'))
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
