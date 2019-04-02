# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfs(MakefilePackage):
    """Squashfs - read only compressed filesystem"""

    homepage = 'http://squashfs.sourceforge.net'
    url      = 'https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz'

    # version      sha1
    version('4.3', 'a615979db9cee82e4a934a1455577f597d290b41')
    version('4.2', 'e0944471ff68e215d3fecd464f30ea6ceb635fd7')
    version('4.1', '7f9b1f9839b3638882f636fd170fd817d650f856')
    version('4.0', '3efe764ac27c507ee4a549fc6507bc86ea0660dd')

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
