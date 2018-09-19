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


class PySfepy(PythonPackage):
    """SfePy (http://sfepy.org) is a software for solving systems of coupled
    partial differential equations (PDEs) by the finite element method in 1D,
    2D and 3D. It can be viewed both as black-box PDE solver, and as a Python
    package which can be used for building custom applications.
    """

    homepage = "http://sfepy.org"
    url      = "https://github.com/sfepy/sfepy/archive/release_2017.3.tar.gz"

    version('2017.3', '65ab606a9fe80fccf17a7eb5ab8fd025')

    variant('petsc', default=False, description='Enable PETSc support')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-sympy', type='run')
    depends_on('hdf5+hl', type='run')
    depends_on('py-pytables', type='run')
    depends_on('py-petsc4py', type='run', when='+petsc')
