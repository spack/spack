# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Squashfs(MakefilePackage):
    """Squashfs - read only compressed filesystem"""

    homepage = 'http://squashfs.sourceforge.net'
    url      = 'https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz'

    # version      md5sum
    version('4.3', 'd92ab59aabf5173f2a59089531e30dbf')
    version('4.2', '1b7a781fb4cf8938842279bd3e8ee852')
    version('4.1', '8e1b2b96f5d5f3fe48fef226ae8cd341')
    version('4.0', 'a3c23391da4ebab0ac4a75021ddabf96')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    def build(self, spec, prefix):
        with working_dir('squashfs-tools'):
            make(parallel=False)

    def install(self, spec, prefix):
        with working_dir('squashfs-tools'):
            make('install', 'INSTALL_DIR=%s' % prefix, parallel=False)
