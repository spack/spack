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


class Alquimia(CMakePackage):
    """Alquimia is an interface that exposes the capabilities
    of mature geochemistry codes such as CrunchFlow and PFLOTRAN"""

    homepage = "https://github.com/LBL-EESA/alquimia-dev"

    version('develop', git='https://github.com/LBL-EESA/alquimia-dev.git')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('debug',  default=False,
            description='Builds a debug version of the libraries')

    depends_on('mpi')
    depends_on('hdf5')
    depends_on('pflotran@develop')
    depends_on('petsc@develop')

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend([
            '-DUSE_XSDK_DEFAULTS=YES',
            '-DCMAKE_BUILD_TYPE:STRING=%s' % (
                'DEBUG' if '+debug' in spec else 'RELEASE'),
            '-DXSDK_ENABLE_DEBUG:STRING=%s' % (
                'YES' if '+debug' in spec else 'NO'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DTPL_ENABLE_MPI:BOOL=ON',
            '-DMPI_BASE_DIR:PATH=%s' % spec['mpi'].prefix,
            '-DTPL_ENABLE_HDF5:BOOL=ON',
            '-DXSDK_WITH_PFLOTRAN:BOOL=ON',
            # This is not good.  It assumes that the .a file exists and is not a .so
            '-DTPL_PFLOTRAN_LIBRARIES=%s' % (
                spec['pflotran'].prefix.lib + "/libpflotranchem.a"),
            '-DTPL_PFLOTRAN_INCLUDE_DIRS=%s' % spec['pflotran'].prefix.include,
            '-DTPL_ENABLE_PETSC:BOOL=ON',
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % self.prefix 
        ])

        return options
