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


class Cdo(AutotoolsPackage):
    """CDO is a collection of command line Operators to manipulate and analyse
    Climate and NWP model Data.
    """

    homepage = "https://code.zmaw.de/projects/cdo"
    url      = "https://code.zmaw.de/attachments/download/12760/cdo-1.7.2.tar.gz"
    list_url = "https://code.zmaw.de/projects/cdo/files"

    version('1.7.2', 'f08e4ce8739a4f2b63fc81a24db3ee31',
            url='https://code.zmaw.de/attachments/download/12760/cdo-1.7.2.tar.gz')
    version('1.6.9', 'bf0997bf20e812f35e10188a930e24e2',
            url='https://code.zmaw.de/attachments/download/10198/cdo-1.6.9.tar.gz')

    variant(
        'enable',
        default='',
        description='Enable support for various tools',
        values=('szip', 'hdf5', 'netcdf', 'udunits2', 'grib', 'libxml2', 'proj', 'curl', 'fftw', 'magics'),  # NOQA: ignore=E501
        exclusive=False
    )

    depends_on('szip', when='enable=szip')
    depends_on('netcdf', when='enable=netcdf')
    depends_on('hdf5+threadsafe', when='enable=hdf5')
    depends_on('udunits2', when='enable=udunits2')
    depends_on('grib-api', when='enable=grib')
    depends_on('libxml2', when='enable=libxml2')
    depends_on('proj', when='enable=proj')
    depends_on('curl', when='enable=curl')
    depends_on('fftw', when='enable=fftw')
    depends_on('magics', when='enable=magics')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-shared',
            '--enable-static'
        ]
        config_args.extend(
            self.with_or_without('enable', lambda x: spec[x].prefix)
        )
        return config_args
