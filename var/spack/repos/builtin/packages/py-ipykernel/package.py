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


class PyIpykernel(PythonPackage):
    """IPython Kernel for Jupyter"""

    homepage = "https://pypi.python.org/pypi/ipykernel"
    url      = "https://github.com/ipython/ipykernel/archive/4.5.0.tar.gz"

    version('4.5.0', 'ea6aaf431b100452905aaca208edac72')
    version('4.4.1', 'c0033e524aa9e05ed18879641ffe6e0f')
    version('4.4.0', '8e626a1708ceff83412180d2ff2f3e57')
    version('4.3.1', '971eee85d630eb4bafcd52531c79673f')
    version('4.3.0', '5961164fe908faf798232a265ed48c73')
    version('4.2.2', '4ac8ae11f1eef4920bf4a5383e13ab50')
    version('4.2.1', 'de583ee9c84db6296269ce7de0afb63f')
    version('4.2.0', 'fc535e4e020a41cd2b55508302b155bb')
    version('4.1.1', '51376850c46fb006e1f8d1cd353507c5')
    version('4.1.0', '638a43e4f8a15872f749090c3f0827b6')

    depends_on('python@2.7:2.7.999,3.3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-traitlets@4.1.0:', type=('build', 'run'))
    depends_on('py-tornado@4.0:', type=('build', 'run'))
    depends_on('py-ipython@4.0:', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-pexpect', type=('build', 'run'))
