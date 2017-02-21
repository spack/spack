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


class PySlepc4py(PythonPackage):
    """This package provides Python bindings for the SLEPc package.
    """
    homepage = "https://pypi.python.org/pypi/slepc4py"
    url      = "https://pypi.python.org/packages/b4/dd/116fbdf865f6f9eda779c5d31bc5b68f37ef3dd5dbfc3feb4aaba1565560/slepc4py-3.7.0.tar.gz"

    version('3.7.0', 'c4775e88b0825c7313629c01de60ecb2')

    depends_on('py-setuptools', type='build')
    depends_on('py-petsc4py', type=('build', 'run'))
    depends_on('slepc')