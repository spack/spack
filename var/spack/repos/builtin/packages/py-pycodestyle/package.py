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


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    url      = "https://github.com/PyCQA/pycodestyle/archive/2.0.0.tar.gz"

    version('2.0.0', '5c3e90001f538bf3b7896d60e92eb6f6')
    version('1.7.0', '31070a3a6391928893cbf5fa523eb8d9')
    version('1.6.2', '8df18246d82ddd3d19ffe7518f983955')
    version('1.6.1', '9d59bdc7c60f46f7cee86c732e28aa1a')
    version('1.6',   '340fa7e39bb44fb08db6eddf7cdc880a')
    version('1.5.7', '6d0f5fc7d95755999bc9275cad5cbf3e')
    version('1.5.6', 'c5c30e3d267b48bf3dfe7568e803a813')
    version('1.5.5', 'cfa12df9b86b3a1dfb13aced1927e12f')
    version('1.5.4', '3977a760829652543544074c684610ee')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
