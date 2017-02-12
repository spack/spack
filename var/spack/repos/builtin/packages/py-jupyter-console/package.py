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


class PyJupyterConsole(PythonPackage):
    """Jupyter Terminal Console"""

    homepage = "https://github.com/jupyter/jupyter_console"
    url      = "https://github.com/jupyter/jupyter_console/archive/5.0.0.tar.gz"

    version('5.0.0', '08a9fde32a45c9e2e0b4cec6eca249c2')
    version('4.1.1', 'a8b077ae0a5c57e9518ac039ad5febb8')
    version('4.1.0', '9c655076262760bdbeeada9d7f586237')
    version('4.0.3', '0e928ea261e7f8154698cf69ed4f2459')
    version('4.0.2', 'f2e174938c91136549b908bd39fa5d59')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.7.999,3.3:')
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-prompt-toolkit@1.0.0:1.999.999', type=('build', 'run'))
