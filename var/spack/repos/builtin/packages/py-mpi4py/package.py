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


class PyMpi4py(PythonPackage):
    """This package provides Python bindings for the Message Passing
       Interface (MPI) standard. It is implemented on top of the
       MPI-1/MPI-2 specification and exposes an API which grounds on the
       standard MPI-2 C++ bindings.
    """
    homepage = "https://pypi.python.org/pypi/mpi4py"
    url      = "https://pypi.io/packages/source/m/mpi4py/mpi4py-3.0.0.tar.gz"
    git      = "https://github.com/mpi4py/mpi4py.git"

    version('develop', branch='master')
    version('3.0.0', 'bfe19f20cef5e92f6e49e50fb627ee70')
    version('2.0.0', '4f7d8126d7367c239fd67615680990e3')
    version('1.3.1', 'dbe9d22bdc8ed965c23a7ceb6f32fc3c')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-setuptools', type='build')
    depends_on('mpi')
    depends_on('py-cython', when='@develop', type='build')
