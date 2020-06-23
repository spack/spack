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

    depends_on('texinfo', type='build')
    depends_on('pip', type=('build', 'link', 'run'))

    def install(self, spec, prefix):
        bash = which('bash')
        bash('build.sh',
             '--prefix=%s' % prefix,
             '--with-glibc-libdir=%s/lib' % prefix_glibc,
             '--with-pip=%s' % prefix_pip)
