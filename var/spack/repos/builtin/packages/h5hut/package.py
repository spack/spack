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


class H5hut(Package):
    """H5hut (HDF5 Utility Toolkit)
    High-Performance I/O Library for Particle-based Simulations
    """

    homepage = "https://amas.psi.ch/H5hut/"
    url      = "https://amas.psi.ch/H5hut/raw-attachment/wiki/DownloadSources/H5hut-1.99.13.tar.gz"

    version("1.99.13", "2a07a449afe50534de006ac6954a421a")

    variant("fortran", default=True, description="Enable Fortran support")
    variant("mpi", default=False, description="Enable MPI support")

    depends_on("autoconf @2.60:", type="build")
    depends_on("automake", type="build")
    depends_on("hdf5 +mpi", when="+mpi")
    depends_on("hdf5 @1.8:")
    # h5hut +mpi uses the obsolete function H5Pset_fapl_mpiposix:
    depends_on("hdf5 @:1.8.12", when="+mpi")
    depends_on("libtool", type="build")
    depends_on("mpi", when="+mpi")

    def install(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()
        configopts = ["--prefix={0}".format(prefix)]
        if "+fortran" in spec:
            if not self.compiler.fc:
                raise RuntimeError(
                    "Cannot build Fortran variant without a Fortran compiler")
            configopts.append("--enable-fortran")
        if "+mpi" in spec:
            configopts.extend([
                "--enable-parallel",
                "CC=%s" % spec["mpi"].mpicc,
                "CXX=%s" % spec["mpi"].mpicxx])
            if "+fortran" in spec:
                configopts.append("FC=%s" % spec["mpi"].mpifc)
        configure(*configopts)

        make()
        make("install")
