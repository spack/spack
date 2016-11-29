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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cmor
#
# You can edit this file again by typing:
#
#     spack edit cmor
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Cmor(Package):

    """Climate Model Output Rewriter Version 3"""

    homepage = "http://cmor.llnl.gov/"
    url  = "https://github.com/PCMDI/cmor"

    version('3.1.2', git="https://github.com/PCMDI/cmor.git", commit='f599ddcd56fa9037e3900cecad859dfc36d36f31')

    variant('uuid', default=True, description='Enable UUID support')
    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('udunits2', default=True, description='Enable UDUNITS2 support')
    variant('hdf5', default=True, description='Enable HDF5 support')   
    variant('python', default=False, description='Enable PYTHON support')
    variant('py-numpy', default=False, description='Enable NUMPY-PYTHON support')

    depends_on('uuid')
    depends_on('netcdf')
    depends_on('udunits2')
    depends_on('hdf5')
    # depends_on('python', when='+python')
    depends_on('py-numpy', when='+python')

    extends('python', when='+python')

    def install(self, spec, prefix):

	config_args = ['--prefix=' + prefix]


	if '+python' in spec:
		config_args.append('--with-python={0}'.format(spec['python'].prefix))

        configure(*config_args)

	if '+python' in spec:
		make('python')
	else:
		make()

	make('install')

