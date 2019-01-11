# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnupg(AutotoolsPackage):
    """GnuPG is a complete and free implementation of the OpenPGP
       standard as defined by RFC4880 """

    homepage = "https://gnupg.org/index.html"
    url = "https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.3.tar.bz2"

    version('2.2.3', '6911c0127e4231ce52d60f26029dba68')
    version('2.1.21', '685ebf4c3a7134ba0209c96b18b2f064')

    depends_on('libgcrypt')
    depends_on('libassuan')
    depends_on('libksba')
    depends_on('libgpg-error')
    depends_on('npth')

    def configure_args(self):
        args = ['--with-npth-prefix=%s' % self.spec['npth'].prefix,
                '--with-libgcrypt-prefix=%s' % self.spec['libgcrypt'].prefix,
                '--with-libksba-prefixx=%s' % self.spec['libksba'].prefix,
                '--with-libassuan-prefix=%s' % self.spec['libassuan'].prefix,
                '--with-libpgp-error-prefix=%s' %
                self.spec['libgpg-error'].prefix]
        return args
