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


class PySingledispatch(PythonPackage):
    """This library brings functools.singledispatch to Python 2.6-3.3."""

    homepage = "https://pypi.python.org/pypi/singledispatch"
    url      = "https://pypi.io/packages/source/s/singledispatch/singledispatch-3.4.0.3.tar.gz"

    version('3.4.0.3', 'af2fc6a3d6cc5a02d0bf54d909785fcb')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))

    # This dependency breaks concretization
    # See https://github.com/LLNL/spack/issues/2793
    # depends_on('py-ordereddict', when="^python@:2.6.999", type=('build', 'run'))  # noqa
