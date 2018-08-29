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


class Libquo(AutotoolsPackage):

    """QUO (as in "status quo") is a runtime library that aids in accommodating
    thread-level heterogeneity in dynamic, phased MPI+X applications comprising
    single- and multi-threaded libraries."""

    homepage = "https://github.com/lanl/libquo"
    url      = "http://lanl.github.io/libquo/dists/libquo-1.3.tar.gz"
    git      = "https://github.com/lanl/libquo.git"

    version('develop', branch='master')
    version('1.3',   '1a1fb83d2c9e99ef5d5fcd71037ef8e8')
    version('1.2.9', '85907cfbdb8b1e57fc5fcf3bced7cfa8')

    depends_on('mpi')

    depends_on('m4',       when='@develop', type='build')
    depends_on('autoconf', when='@develop', type='build')
    depends_on('automake', when='@develop', type='build')
    depends_on('libtool',  when='@develop', type='build')

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen')

    def configure_args(self):
        return [
            'CC={0}'.format(self.spec['mpi'].mpicc),
            'FC={0}'.format(self.spec['mpi'].mpifc)
        ]
