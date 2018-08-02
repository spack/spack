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


class NetcdfFortran(AutotoolsPackage):
    """Fortran interface for NetCDF4"""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.4.3.tar.gz"

    version('4.4.4', 'e855c789cd72e1b8bc1354366bf6ac72')
    version('4.4.3', 'bfd4ae23a34635b273d3eb0d91cbde9e')

    depends_on('netcdf')

    # The default libtool.m4 is too old to handle NAG compiler properly:
    # https://github.com/Unidata/netcdf-fortran/issues/94
    patch('nag.patch', when='@:4.4.4%nag')

    def configure_args(self):
        return ['CPPFLAGS=-I' + self.spec['netcdf'].prefix.include]

    @property
    def libs(self):
        libraries = ['libnetcdff']

        # This package installs both shared and static libraries. Permit
        # clients to query which one they want.
        query_parameters = self.spec.last_query.extra_parameters
        shared = 'shared' in query_parameters

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )
