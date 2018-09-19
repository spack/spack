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


class EtsfIo(Package):
    """ETSF_IO is a library implementing the Nanoquanta/ETSF file
    format specifications.

    ETSF_IO enables an architecture-independent exchange of crystallographic
    data, electronic wavefunctions, densities and potentials, as well as
    spectroscopic data. It is meant to be used by quantum-physical and
    quantum-chemical applications relying upon Density Functional Theory (DFT).
    """

    homepage = "http://www.etsf.eu/resources/software/libraries_and_tools"
    url = "https://launchpad.net/etsf-io/1.0/1.0.4/+download/etsf_io-1.0.4.tar.gz"

    version('1.0.4', '32d0f7143278bd925b334c69fa425da1')

    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi~cxx", when='+mpi')  # required for NetCDF-4 support

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        oapp = options.append

        # Specify installation directory for Fortran module files
        # Default is [INCLUDEDIR/FC_TYPE]
        oapp("--with-moduledir=%s" % prefix.include)

        # Netcdf4/HDF
        hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf5"].prefix.lib
        options.extend([
            "--with-netcdf-incs=-I%s" % spec["netcdf-fortran"].prefix.include,
            "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf %s" % (
                spec["netcdf-fortran"].prefix.lib, hdf_libs),
        ])

        configure(*options)

        make()
        make("check")
        make("install")
