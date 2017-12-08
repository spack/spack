##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Nalu(CMakePackage):
    """Nalu: a generalized unstructured massively parallel low Mach flow code
       designed to support a variety of energy applications of interest (most
       notably Wind ECP) built on the Sierra Toolkit and Trilinos solver
       Tpetra/Epetra stack
    """

    homepage = "https://github.com/NaluCFD/Nalu"
    url      = "https://github.com/NaluCFD/Nalu.git"

    maintainers = ['jrood-nrel']

    variant('openfast', default=False,
            description='Compile with OpenFAST support')
    variant('tioga', default=False,
            description='Compile with Tioga support')

    version('master',
            git='https://github.com/NaluCFD/Nalu.git', branch='master')

    # Currently Nalu only builds static libraries; To be fixed soon
    depends_on('yaml-cpp+pic~shared@0.5.3:')
    depends_on('trilinos~shared+exodus+tpetra+muelu+belos+ifpack2+amesos2+zoltan+stk+boost~superlu-dist+superlu+hdf5+zlib+pnetcdf+shards@master,12.12.1:')
    depends_on('openfast+cxx', when='+openfast')
    depends_on('tioga', when='+tioga')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DTrilinos_DIR:PATH=%s' % spec['trilinos'].prefix,
            '-DYAML_DIR:PATH=%s' % spec['yaml-cpp'].prefix,
            '-DENABLE_INSTALL:BOOL=ON'
        ])

        if '+openfast' in spec:
            options.extend([
                '-DENABLE_OPENFAST:BOOL=ON',
                '-DOpenFAST_DIR:PATH=%s' % spec['openfast'].prefix
            ])

        if '+tioga' in spec:
            options.extend([
                '-DENABLE_TIOGA:BOOL=ON',
                '-DTIOGA_DIR:PATH=%s' % spec['tioga'].prefix
            ])

        return options
