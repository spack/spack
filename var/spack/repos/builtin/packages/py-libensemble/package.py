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


class PyLibensemble(PythonPackage):
    """Library for managing ensemble-like collections of computations."""

    homepage = "https://libensemble.readthedocs.io"
    url      = "https://pypi.io/packages/source/l/libensemble/libensemble-0.2.0.tar.gz"
    git      = "https://github.com/Libensemble/libensemble.git"

    version('develop', branch='master')
    version('0.2.0', 'ee96047594a3f5a1533f24d3b1f365f9')
    version('0.1.0', '0c3d45dd139429de1a5273e5bd8e46ec')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-setuptools', type='build')
    depends_on('mpi')
    depends_on('py-mpi4py@2.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-petsc4py@3.5:', type=('build', 'run'))
    depends_on('nlopt', type=('build', 'run'))
