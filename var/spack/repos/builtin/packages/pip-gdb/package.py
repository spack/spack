# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PipGdb(Package):
    """GDB for PiP"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP-gdb"
    git      = "https://github.com/RIKEN-SysSoft/PiP-gdb.git"

    version('1', branch='pip-centos7')

    patch('disable-werror.patch')

    depends_on('texinfo', type='build')
    depends_on('pip', type='build')

    def install(self, spec, prefix):
        glibc_prefix = spec['pip-glibc'].prefix
        glibc_dir = join_path(join_path(glibc_prefix, 'pip-glibc'), 'lib')
        bash = which('bash')
        bash('build.sh',
             '--prefix=%s' % prefix,
             '--with-glibc-libdir=%s' % glibc_dir,
             '--with-pip=%s' % spec['pip'].prefix)
