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


class Libquo(AutotoolsPackage):

    """QUO (as in "status quo") is a runtime library that aids in accommodating
    thread-level heterogeneity in dynamic, phased MPI+X applications comprising
    single- and multi-threaded libraries."""

    homepage = "https://github.com/lanl/libquo"
    url      = "https://github.com/lanl/libquo/archive/v1.2.9.tar.gz"

    version('1.2.9', 'ca82ab33f13e2b89983f81e7c02e98c2')

    depends_on('mpi')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    def configure_args(self):
        return [
            'CC={0}'.format(self.spec['mpi'].mpicc),
            'FC={0}'.format(self.spec['mpi'].mpifc)
        ]
