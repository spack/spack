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


class Mvdtool(CMakePackage):
    """MVD3 neuroscience file format parser and tool"""

    homepage = "https://github.com/BlueBrain/MVDTool"
    url      = "https://github.com/BlueBrain/MVDTool.git"

    version('develop', git=url)
    version('1.5', git=url, tag='v1.5', preferred=True)
    version('1.4', git=url, tag='v1.4')

    variant('mpi', default=True, description="Enable MPI backend")
    variant('python', default=False, description="Enable Python bindings")

    depends_on('boost')
    depends_on('cmake', type='build')

    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')

    depends_on('python', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(self.spec['mpi'].mpicxx),
            ])
        if self.spec.satisfies('+python'):
            args.extend([
                '-DBUILD_PYTHON_BINDINGS:BOOL=ON'
            ])
        return args
