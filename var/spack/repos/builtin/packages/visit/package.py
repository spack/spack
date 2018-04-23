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


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
       animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz"

    version('2.13.0', '716644b8e78a00ff82691619d4d1e7a914965b6535884890b667b97ba08d6a0f')
    version('2.12.3', '2dd351a291ee3e79926bc00391ca89b202cfa4751331b0fdee1b960c7922161f')
    version('2.12.2', '355779b1dbf440cdd548526eecd77b60')
    version('2.10.3', 'a1082a6f6dab3e2dcb58993603456c2b')
    version('2.10.2', '253de0837a9d69fb689befc98ea4d068')
    version('2.10.1', '3cbca162fdb0249f17c4456605c4211e')

    depends_on('cmake@3.0:', type='build')
    depends_on('vtk@6.1.0~opengl2')
    depends_on('qt@4.8.6')
    depends_on('qwt')
    depends_on('python')
    depends_on('silo+shared')
    depends_on('hdf5')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec
        qt_bin = spec['qt'].prefix.bin
        args = [
            '-DVTK_MAJOR_VERSION={0}'.format(spec['vtk'].version[0]),
            '-DVTK_MINOR_VERSION={0}'.format(spec['vtk'].version[1]),
            '-DVISIT_VTK_DIR:PATH={0}'.format(spec['vtk'].prefix),
            '-DVISIT_USE_GLEW=OFF',
            '-DVISIT_LOC_QMAKE_EXE:FILEPATH={0}/qmake-qt4'.format(qt_bin),
            '-DPYTHON_DIR:PATH={0}'.format(spec['python'].home),
            '-DVISIT_SILO_DIR:PATH={0}'.format(spec['silo'].prefix),
            '-DVISIT_HDF5_DIR:PATH={0}'.format(spec['hdf5'].prefix),
            '-DVISIT_QWT_DIR:PATH={0}'.format(spec['qwt'].prefix)
        ]

        if spec.satisfies('^hdf5+mpi', strict=True):
            args.append('-DVISIT_HDF5_MPI_DIR:PATH={0}'.format(
                spec['hdf5'].prefix))

        return args
