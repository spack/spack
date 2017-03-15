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


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://pypi.python.org/pypi/traitlets"
    url      = "https://github.com/ipython/traitlets/archive/4.3.1.tar.gz"

    version('4.3.1', '146a4885ea64079f62a33b2049841543')
    version('4.3.0', '17af8d1306a401c42dbc92a080722422')
    version('4.2.2', 'ffc03056dc5c8d1fc5dbd6eac76e1e46')
    version('4.2.1', 'fc7f46a76b99ebc5068f99033d268dcf')
    version('4.2.0', '53553a10d124e264fd2e234d0571b7d0')
    version('4.1.0', 'd5bc75c7bd529afb40afce86c2facc3a')
    version('4.0.0', 'b5b95ea5941fd9619b4704dfd8201568')
    version('4.0',   '14544e25ccf8e920ed1cbf833852481f')

    depends_on('py-setuptools', type='build')
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))

    # This dependency breaks concretization
    # See https://github.com/LLNL/spack/issues/2793
    # depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'))
