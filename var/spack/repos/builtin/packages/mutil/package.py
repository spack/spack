# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.pkg.builtin.coreutils import Coreutils as CoreutilsSpack


class Mutil(CoreutilsSpack):
    """Mutil provides mcp and msum, which are drop-in replacements for cp
       and md5sum that utilize multiple types of parallelism to achieve
       maximum copy and checksum performance on clustered file systems.
    """
    homepage = "Multi-threaded cp and md5sum based on GNU coreutils"
    url      = "http://ftp.gnu.org/gnu/coreutils/coreutils-8.26.tar.xz"

    version('8.22', '8fb0ae2267aa6e728958adc38f8163a2', preferred=True)

    build_directory = 'spack-build'

    depends_on('gnutls')
    depends_on('libgcrypt')
    depends_on('libgpg-error')
    depends_on('mpi')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('gettext', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    resource(
       name='mutil',
       git='https://github.com/pkolano/mutil.git',
       commit='a60175eba0f02b4674a7dadeaf168d035aace851',
    )

    @run_before('autoreconf')
    def enable_mutil(self):
        patch = which('patch')
        patch("-p1", "--input=mutil/patch/coreutils-8.22.patch")
        # The patch touches the configure script which means the
        # force_autoreconf option won't work correctly so we
        # remove it manually here
        os.remove('configure')

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.share.man.man1)
        install('spack-build/src/cp',
                '{0}/mcp'.format(self.prefix.bin))
        install('spack-build/src/md5sum',
                '{0}/msum'.format(self.prefix.bin))
        install('spack-build/man/cp.1',
                '{0}/mcp.1'.format(self.prefix.share.man.man1))
        install('spack-build/man/md5sum.1',
                '{0}/msum.1'.format(self.prefix.share.man.man1))
