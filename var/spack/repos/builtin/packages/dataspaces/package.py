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
#     spack install dataspaces
#
# You can edit this file again by typing:
#
#     spack edit dataspaces
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from subprocess import call

class Dataspaces(AutotoolsPackage):
    """an extreme scale data management framework."""

    homepage = "http://www.dataspaces.org"
    url      = "http://personal.cac.rutgers.edu/TASSL/projects/data/downloads/dataspaces-1.6.1.tar.gz"

    version('1.6.1', '1866b0a6c4c95714adcedec32ee212ac')

    variant('dimes', 
        default=False, 
        description='enabled DIMES transport mode')

    variant('infiniband',
            default=False,
            description='enabled infiniband transport fabric')

    variant('ugni',
            default=False,
            description='enabled Cray uGNI transport fabric')

    variant('tcp',
            default=True,
            description='enabled TCP socket transport')

    variant('piclibs',
        default=False,
        description='Build PIC versions of dataspaces libraries')

    # FIXME: Add dependencies if required.
    depends_on('m4')
    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool')

    def autoreconf(spec, prefix, self):
        call(['sh', './autogen.sh'])

    def configure_args(self):
        args = ['CC=mpicc','FC=mpif90','LIBS=-lpthread -lm']
	if self.spec.satisfies('+dimes'):
	    args.extend(['--enable-dimes'])
	return args
