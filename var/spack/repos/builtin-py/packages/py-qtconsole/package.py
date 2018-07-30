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


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "http://ipython.org"
    url      = "https://pypi.io/packages/source/q/qtconsole/qtconsole-4.2.1.tar.gz"

    version('4.2.1', 'c08ebebc7a60629ebadf685361ca0798')

    variant('doc', default=False, description='Build documentation')

    depends_on('py-ipykernel@4.1:',      type=('build', 'run'))
    depends_on('py-jupyter-client@4.1:', type=('build', 'run'))
    depends_on('py-jupyter-core',        type=('build', 'run'))
    depends_on('py-pygments',            type=('build', 'run'))
    depends_on('py-traitlets',           type=('build', 'run'))
    depends_on('py-sphinx@1.3:',         type=('build', 'run'), when='+docs')

    depends_on('py-mock', type='test', when='^python@2.7:2.8')
