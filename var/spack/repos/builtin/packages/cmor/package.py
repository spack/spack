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


class Cmor(AutotoolsPackage):
    """Climate Model Output Rewriter is used to produce CF-compliant netCDF
    files. The structure of the files created by the library and the metadata
    they contain fulfill the requirements of many of the climate community's
    standard model experiments."""

    homepage = "http://cmor.llnl.gov"
    url = "https://github.com/PCMDI/cmor/archive/3.1.2.tar.gz"

    version('3.2.0', 'b48105105d4261012c19cd65e89ff7a6')
    version('3.1.2', '72f7227159c901e4bcf80d2c73a8ce77')

    variant('fortran', default=True, description='Enable Fortran API')
    variant('python', default=False, description='Enable PYTHON support')

    depends_on('uuid')
    depends_on('netcdf')
    depends_on('udunits2')
    depends_on('hdf5@:1.8')

    extends('python', when='+python')
    depends_on('python@:2.7', when='+python')
    depends_on('py-numpy', type=('build', 'run'), when='+python')

    @run_before('configure')
    def validate(self):
        if '+fortran' in self.spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

    def configure_args(self):
        extra_args = ['--disable-debug']

        if '+fortran' in self.spec:
            extra_args.append('--enable-fortran')
        else:
            extra_args.append('--disable-fortran')

        return extra_args

    def install(self, spec, prefix):
        make('install')

        if '+python' in spec:
            setup_py('install', '--prefix=' + prefix)
