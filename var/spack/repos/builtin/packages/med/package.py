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


class Med(CMakePackage):
    """The MED file format is a specialization of the HDF5 standard."""

    homepage = "http://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url      = "http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz"

    version('3.2.0', 'eb61df92f0624feb6328f517cd756a23')

    depends_on('hdf5@:1.8.19')

    # FIXME This is minimal installation.

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_CXX_FLAGS:STRING=%s' % '-DMED_API_23=1',
            '-DCMAKE_C_FLAGS:STRING=%s' % '-DMED_API_23=1',
            '-DMEDFILE_BUILD_TESTS=OFF',
            '-DMEDFILE_BUILD_PYTHON=OFF',
            '-DMEDFILE_INSTALL_DOC=OFF',
            '-DMEDFILE_BUILD_SHARED_LIBS=OFF',
            '-DMEDFILE_BUILD_STATIC_LIBS=ON',
            '-DCMAKE_Fortran_COMPILER=',
            '-DMED_API_23=1',
            '-DHDF5_ROOT_DIR=%s' % spec['hdf5'].prefix
        ]
        return args
