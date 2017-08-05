##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package."""

    homepage = "https://pypi.python.org/pypi/petsc4py"
    url      = "https://pypi.io/packages/source/p/petsc4py/petsc4py-3.7.0.tar.gz"

    version('3.7.0', '816a20040a6a477bd637f397c9fb5b6d')

    variant('mpi', default=True, description='Enable MPI support')

    # Python version 2.6, 2.7 or >= 3.2 required
    extends('python@2.6:2.8,3.2:')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.22:', type='build')
    depends_on('py-numpy', type=('build', 'link', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'), when='+mpi')

    # Major and minor version must match
    depends_on('petsc')
    depends_on('petsc+mpi', when='+mpi')
    depends_on('petsc@3.7.0:3.7.999', when='@3.7.0:3.7.999')
