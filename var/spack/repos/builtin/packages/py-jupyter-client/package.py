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


class PyJupyterClient(PythonPackage):
    """Jupyter protocol client APIs"""

    homepage = "https://github.com/jupyter/jupyter_client"
    url      = "https://github.com/jupyter/jupyter_client/archive/4.4.0.tar.gz"

    version('4.4.0', 'a0bd6fe6ba7c504fbc962a88a2a56a90')
    version('4.3.0', '257d9f5429dac4d9511db84d201d3a9e')
    version('4.2.2', '988ea87554215a83c6ad52e554d8d8c4')
    version('4.2.1', '16994e5cace322c777456bc5a26502d7')
    version('4.2.0', '61c43c9f243e42f1945fae5d56d0d23c')
    version('4.1.1', '8436e4a3266a442f576cdfef39dc0e19')
    version('4.1.0', 'cf42048b889c8434fbb5813a9eec1d34')
    version('4.0.0', '00fa63c67cb3adf359d09dc4d803aff5')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.7.999,3.3:')
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-zmq@13:', type=('build', 'run'))
