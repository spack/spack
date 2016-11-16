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


class Nco(Package):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "https://sourceforge.net/projects/nco"
    url      = "https://github.com/nco/nco/archive/4.5.5.tar.gz"

    version('4.6.1', 'ef43cc989229c2790a9094bd84728fd8')
    version('4.5.5', '9f1f1cb149ad6407c5a03c20122223ce')

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    variant('mpi', default=True)

    depends_on('netcdf')
    depends_on('antlr@2.7.7+cxx')  # required for ncap2
    depends_on('gsl')              # desirable for ncap2
    depends_on('udunits2')         # allows dimensional unit transformations
    # depends_on('opendap')        # enables network transparency

    def install(self, spec, prefix):
        # Workaround until variant forwarding works properly
        if '+mpi' in spec and spec.satisfies('^netcdf~mpi'):
            raise RuntimeError('Invalid spec. Package netcdf requires '
                               'netcdf+mpi, but spec asked for netcdf~mpi.')

        opts = [
            '--prefix=%s' % prefix,
            '--disable-openmp',  # TODO: Make this a variant
            '--disable-dap',     # TODO: Make this a variant
            '--disable-esmf']
        configure(*opts)
        make()
        make("install")
