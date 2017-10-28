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
    """A Multi-purpose, Application-Centric, Scalable I/O Proxy Application"""

    homepage = "http://llnl.github.io/MACSio"

    # NOTE: macsio-v0.9 is build with gmake and is not properly built here.
    # url = "https://github.com/LLNL/MACSio/releases/download/v0.9/macsio-0.9.tar.gz"
    # version('0.9', '6d4bf863c90975a3df54795c5abb9eb8f23d5aaf')

    version('master', git='https://github.com/LLNL/MACSio.git', branch='cmake2')
    depends_on('json-cwx')

    ## TODO: Test these and add these to spack!

    variant('mpi', default=False, description="Build MPI plugin")
    depends_on('mpi', when="+mpi")

    variant('silo', default=False, description="Build with SILO plugin")
    depends_on('silo', when="+silo")

    variant('hdf5', default=False, description="Build HDF5 plugin")
    depends_on('hdf5', when="+hdf5")

    variant('pdb', default=False, description="Build PDB plugin")
    depends_on('pdb', when="+pdb")

    variant('exodus', default=False, description="Build EXODUS plugin")
    depends_on('exodus', when="+exodus")

    variant('typhonio', default=False, description="Build TYPHONIO plugin")
    depends_on('typhonio', when="+typhonio")

    variant('scr', default=False, description="Build with SCR support")
    depends_on('scr', when="+scr")


    def get_abs_path_rel_prefix(self, path):
        # Return path if absolute, otherwise prepend prefix
        if os.path.isabs(path):
            return path
        else:
            return join_path(self.spec.prefix, path)

    def cmake_args(self):
        spec = self.spec
        args = []

        if "+silo" in spec:
            args.apprend("-DWITH_SILO_PREFIX={0}".format(spec['silo'].prefix))

        # TODO: add proper args
