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


class PyCogent(PythonPackage):
    """A toolkit for statistical analysis of biological sequences."""

    homepage = "http://pycogent.org"
    url      = "https://pypi.io/packages/source/c/cogent/cogent-1.9.tar.gz"

    version('1.9', '7d9f28cd17664c1cd18c568fc53060d6')
    version('1.5.3', sha256='4e19325cd1951382dc71582eb49f44c5a19eb128e3540e29dc28e080091e49cd')

    variant('matplotlib', default=False, description="graphs related to codon usage")
    variant('cython', default=False, description="This module is only necessary .pyx files.")
    variant('mpi4py', default=False, description='MPI required for parallel computation.')
    variant('sqlalchemy', default=False, description='Required for the Ensembl querying code.')

    depends_on('python@2.6:2.999', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('zlib')
    depends_on('py-matplotlib', when='+py-matplotlib', type=('build', 'run'))
    depends_on('py-cython', when='+py-cython', type=('build', 'run'))
    depends_on('py-mpi4py', when='+py-mpi4py', type=('build', 'run'))
    depends_on('py-sqlalchemy', when='+py-sqlalchemy', type=('build', 'run'))
