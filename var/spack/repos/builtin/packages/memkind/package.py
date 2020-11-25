# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    version('1.7.0', sha256='5048eaaa1bc484203c685a019f3f428ab6c9b1cf94ef6d264e299bc0127ec572')

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
