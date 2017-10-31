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

    version('0.99', git='ttps://github.com/LLNL/MACSio.git', 
            commit='46ef84dd1bcebb663d2d9b8fa58e48bc1cf37f68')
    version('develop', git='https://github.com/LLNL/MACSio.git',
            branch='cmake2')

    depends_on('json-cwx')

    variant('mpi', default=True, description="Build MPI plugin")
    depends_on('mpi', when="+mpi")

    variant('silo', default=True, description="Build with SILO plugin")
    depends_on('silo', when="+silo")

    # TODO: multi-level variants
    variant('hdf5', default=False, description="Build HDF5 plugin")
    depends_on('hdf5', when="+hdf5")
    variant('zfp', default=False, description="Build HDF5 with ZFP compression")
    variant('szip', default=False, description="Build HDF5 with SZIP compression")
    # depends_on('hdf5+szip', when="+szip")
    variant('zlib', default=False, description="Build HDF5 with ZLIB compression")

    # pdb is packaged with silo
    variant('pdb', default=False, description="Build PDB plugin")
    depends_on('silo', when="+pdb")

    variant('exodus', default=False, description="Build EXODUS plugin")
    depends_on('exodusii', when="+exodus")

    # TODO: typhonio not in spack
    # variant('typhonio', default=False, description="Build TYPHONIO plugin")
    # depends_on('typhonio', when="+typhonio")

    variant('scr', default=False, description="Build with SCR support")
    depends_on('scr', when="+scr")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "~mpi" in spec:
            cmake_args.append("-DENABLE_MPI=OFF")

        if "~silo" in spec:
            cmake_args.append("-DENABLE_SILO=OFF")

        if "+silo" in spec:
            cmake_args.append("-DWITH_SILO_PREFIX={0}"
                              .format(spec['silo'].prefix))

        if "+pdb" in spec:
            # pdb is a part of silo
            cmake_args.append("-DENABLE_PDF=ON")
            cmake_args.append("-DWITH_SILO_PREFIX={0}"
                              .format(spec['silo'].prefix))
        if "+hdf5" in spec:
            cmake_args.append("-DENABLE_HDF5=ON")
            cmake_args.append("-DWITH_HDF5_PREFIX={0}"
                              .format(spec['hdf5'].prefix))
            # TODO: Multi-level variants
            # ZFP not in hdf5 spack package??
            # if "+zfp" in spec:
            #     cmake_args.append("-DENABLE_HDF5_ZFP")
            #     cmake_args.append("-DWITH_ZFP_PREFIX={0}"
            #         .format(spec['silo'].prefix))
            # SZIP is an hdf5 spack variant
            # if "+szip" in spec:
            #     cmake_args.append("-DENABLE_HDF5_SZIP")
            #     cmake_args.append("-DWITH_SZIP_PREFIX={0}"
            #         .format(spec['SZIP'].prefix))
            # ZLIB is on by default, @1.1.2
            # if "+zlib" in spec:
            #     cmake_args.append("-DENABLE_HDF5_ZLIB")
            #     cmake_args.append("-DWITH_ZLIB_PREFIX={0}"
            #         .format(spec['silo'].prefix))

        # TODO: typhonio not in spack
        # if "+typhonio" in spec:
        #     cmake_args.append("-DENABLE_TYPHONIO=ON")
        #     cmake_args.append("-DWITH_TYPHONIO_PREFIX={0}"
        #         .format(spec['typhonio'].prefix))

        if "+exodus" in spec:
            cmake_args.append("-DENABLE_EXODUS=ON")
            cmake_args.append("-DWITH_EXODUS_PREFIX={0}"
                              .format(spec['exodusii'].prefix))
            # exodus requires netcdf
            cmake_args.append("-DWITH_NETCDF_PREFIX={0}"
                              .format(spec['netcdf'].prefix))

        return cmake_args
