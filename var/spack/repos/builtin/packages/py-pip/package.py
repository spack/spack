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


class PyPip(PythonPackage):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pypi.python.org/pypi/pip"
    url      = "https://pypi.io/packages/source/p/pip/pip-9.0.1.tar.gz"

    version('9.0.1', '35f01da33009719497f01a4ba69d63c9')

    depends_on('python@2.6:2.7,3.3:')

    # Most Python packages only require setuptools as a build dependency.
    # However, pip requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
