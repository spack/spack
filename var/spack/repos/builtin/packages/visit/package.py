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


class Visit(Package):
    """VisIt is an Open Source, interactive, scalable, visualization, animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz"

    version('2.10.1', '3cbca162fdb0249f17c4456605c4211e')
    version('2.10.2', '253de0837a9d69fb689befc98ea4d068')

    depends_on("vtk@6.1.0~opengl2")
    depends_on("qt@4.8.6")
    depends_on("python")
    depends_on("silo+shared")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):

            feature_args = std_cmake_args[:]
            feature_args.extend(["-DVTK_MAJOR_VERSION=6",
                                 "-DVTK_MINOR_VERSION=1",
                                 "-DVISIT_LOC_QMAKE_EXE:FILEPATH=%s/qmake-qt4" % spec['qt'].prefix.bin,
                                 "-DPYTHON_EXECUTABLE:FILEPATH=%s/python" % spec['python'].prefix.bin,
                                 "-DVISIT_SILO_DIR:PATH=%s" % spec['silo'].prefix,
                                 "-DVISIT_HDF5_DIR:PATH=%s" % spec['hdf5'].prefix])

            cmake('../src', *feature_args)

            make()
            make("install")
