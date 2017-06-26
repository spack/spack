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
from subprocess import call

def is_string(x):
    """validate a string"""
    try:
        return isinstance(x, basestring)
    except ValueError:
        return False

class Dataspaces(AutotoolsPackage):
    """an extreme scale data management framework."""

    homepage = "http://www.dataspaces.org"
    url      = "http://personal.cac.rutgers.edu/TASSL/projects/data/downloads/dataspaces-1.6.2.tar.gz"

    version('develop', git='https://github.com/melrom/dataspaces.git',
            branch='master')
    version('1.6.2', '73caa4920b6f2c0c6d6cb87640ff04be')

    variant('dimes',
        default=False,
        description='enabled DIMES transport mode')
    variant('cray-drc',
        default=False,
        description='using Cray Dynamic Credentials library')
    variant('gni-cookie',
        default='0x5420000',
        description='Cray UGNI communication token',
        values=is_string)
    variant('ptag',
        default='250',
        description='Cray UGNI protection tag',
        values=is_string)
    variant('mpi',
        default=False,
        description='Use MPI for collective communication')


    depends_on('m4')
    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool')
    # spack interal pkg-config seems to cause problems on Titan
    #depends_on('pkg-config')
    depends_on('mpi', when='+mpi')

    def autoreconf(spec, prefix, self):
        call(['sh', './autogen.sh'])

    def configure_args(self):
        args = []
        cookie = self.spec.variants['gni-cookie'].value
        ptag = self.spec.variants['ptag'].value
        if self.spec.satisfies('+dimes'):
            args.extend(['--enable-dimes'])
        if self.spec.satisfies('+cray-drc'):
            args.extend(['--enable-drc'])
        else:
            args.extend(['--with-gni-cookie=%s' % cookie])
            args.extend(['--with-gni-ptag=%s' % ptag])
        if self.spec.satisfies('+mpi'):
            args.extend(['CC=%s' % self.spec['mpi'].mpicc])
            args.extend(['FC=%s' % self.spec['mpi'].mpifc])
        return args
