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


class Nco(AutotoolsPackage):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "http://nco.sourceforge.net/"
    url      = "https://github.com/nco/nco/archive/4.6.5.tar.gz"

    version('4.6.5', '2afd34a6bb5ff6c7ed39cf40c917b6e4')
    version('4.6.4', '22f4e779d0011a9c0db90fda416c8e45')
    version('4.6.3', '0e1d6616c65ed3a30c54cc776da4f987')
    version('4.6.2', 'b7471acf0cc100343392f4171fb56113')
    version('4.6.1', 'ef43cc989229c2790a9094bd84728fd8')
    version('4.5.5', '9f1f1cb149ad6407c5a03c20122223ce')

    variant('doc', default=False, description='Build/install NCO TexInfo-based documentation')

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    depends_on('netcdf')
    depends_on('antlr@2.7.7+cxx')  # required for ncap2
    depends_on('gsl')              # desirable for ncap2
    depends_on('udunits2')         # allows dimensional unit transformations

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('texinfo@4.12:', type='build', when='+doc')

    def configure_args(self):
        spec = self.spec
        return ['--{0}-doc'.format('enable' if '+doc' in spec else 'disable')]
