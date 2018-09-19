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


class H5utils(AutotoolsPackage):
    """h5utils is a set of utilities for visualization and conversion of
    scientific data in the free, portable HDF5 format."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/H5utils"
    url      = "http://ab-initio.mit.edu/h5utils/h5utils-1.12.1.tar.gz"
    list_url = "http://ab-initio.mit.edu/h5utils/old/"

    version('1.12.1', '46a6869fee6e6bf87fbba9ab8a99930e')

    variant('png',    default=True,  description='Enable PNG support')
    variant('vis5d',  default=False, description='Enable Vis5d support')
    variant('octave', default=False, description='Enable GNU Octave support')
    variant('hdf4',   default=False, description='Enable HDF4 support')
    variant('math',   default=False, description='Build h5math')

    # Required dependencies
    depends_on('hdf5')

    # Optional dependencies
    depends_on('libpng',      when='+png')
    # depends_on('vis5d',       when='+vis5d')  # TODO: Add a vis5d package
    depends_on('octave',      when='+octave')
    depends_on('hdf',         when='+hdf4')
    depends_on('libmatheval', when='+math')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+vis5d' in spec:
            args.append('--with-v5d={0}'.format(spec['vis5d'].prefix))
        else:
            args.append('--without-v5d')

        if '+octave' in spec:
            args.append('--with-octave')
        else:
            args.append('--without-octave')

        if '+hdf' in spec:
            args.append('--with-hdf4')
        else:
            args.append('--without-hdf4')

        return args
