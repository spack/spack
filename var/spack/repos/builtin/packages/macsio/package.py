##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Macsio(CMakePackage):
    """A Multi-purpose, Application-Centric, Scalable I/O Proxy Application
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "http://llnl.github.io/MACSio"

    # NOTE: macsio-v0.9 is build with gmake and is not properly built here.
    # url = "https://github.com/LLNL/MACSio/releases/download/v0.9/macsio-0.9.tar.gz"
    # version('0.9', '6d4bf863c90975a3df54795c5abb9eb8f23d5aaf')

    version('develop', git='https://github.com/LLNL/MACSio.git',
            branch='cmake2')

    variant('mpi', default=True, description="Build MPI plugin")
    variant('silo', default=True, description="Build with SILO plugin")
    variant('hdf5', default=False, description="Build HDF5 plugin")
    variant('pdb', default=False, description="Build PDB plugin")
    variant('exodus', default=False, description="Build EXODUS plugin")
    variant('typhonio', default=False, description="Build TYPHONIO plugin")
    variant('scr', default=False, description="Build with SCR support")

    depends_on('mpi', when="+mpi")
    depends_on('json-cwx')
    depends_on('silo', when="+silo")
    depends_on('hdf5', when="+hdf5")
    depends_on('scr', when="+scr")
    depends_on('pdb', when="+pdb")
    depends_on('exodus', when="+exodus")
    depends_on('typhonio', when="+typhonio")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "-mpi" in spec:
            cmake_args.append("-DENABLE_MPI=OFF")

        if "-silo" in spec:
            cmake_args.append("-DENABLE_SILO=OFF")

        if "+silo" in spec:
            cmake_args.append("-DWITH_SILO_PREFIX={0}"
                .format(spec['silo'].prefix))

        return cmake_args
