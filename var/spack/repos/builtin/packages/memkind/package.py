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
import os


class Memkind(AutotoolsPackage):
    """The memkind library is a user extensible heap manager built on top of
    jemalloc which enables control of memory characteristics and a partitioning
    of the heap between kinds of memory. The kinds of memory are defined by
    operating system memory policies that have been applied to virtual address
    ranges. Memory characteristics supported by memkind without user extension
    include control of NUMA and page size features. The jemalloc non-standard
    interface has been extended to enable specialized arenas to make requests
    for virtual memory from the operating system through the memkind partition
    interface. Through the other memkind interfaces the user can control and
    extend memory partition features and allocate memory while selecting
    enabled features."""

    homepage = "https://github.com/memkind/memkind"
    url      = "https://github.com/memkind/memkind/archive/v1.7.0.tar.gz"

    version('1.7.0', 'bfbbb9226d40fd12ae1822a8be4c9207')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('numactl')

    phases = ['build_jemalloc', 'autoreconf', 'configure', 'build',
              'install']

    def patch(self):
        with open('VERSION', 'w') as version_file:
            version_file.write('{0}\n'.format(self.version))

    def build_jemalloc(self, spec, prefix):
        if os.path.exists('build_jemalloc.sh'):
            bash = which('bash')
            bash('./build_jemalloc.sh')

    def autoreconf(self, spec, prefix):
        if os.path.exists('autogen.sh'):
            bash = which('bash')
            bash('./autogen.sh')
