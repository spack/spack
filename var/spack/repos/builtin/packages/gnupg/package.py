# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnupg(AutotoolsPackage):
    """GnuPG is a complete and free implementation of the OpenPGP
       standard as defined by RFC4880 """

    homepage = "https://gnupg.org/index.html"
    url      = "https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.17.tar.bz2"

    version('2.2.17', sha256='afa262868e39b651a2db4c071fba90415154243e83a830ca00516f9a807fd514')
    version('2.2.15', sha256='cb8ce298d7b36558ffc48aec961b14c830ff1783eef7a623411188b5e0f5d454')
    version('2.2.3',  sha256='cbd37105d139f7aa74f92b6f65d136658682094b0e308666b820ae4b984084b4')
    version('2.1.21', sha256='7aead8a8ba75b69866f583b6c747d91414d523bfdfbe9a8e0fe026b16ba427dd')

    depends_on('libgcrypt@1.7.0:')
    depends_on('libassuan@2.4:', when='@:2.2.3')
    depends_on('libassuan@2.5:', when='@2.2.15:')
    depends_on('libksba@1.3.4:')
    depends_on('libgpg-error@1.24:')
    depends_on('npth@1.2:')
    depends_on('zlib')
    depends_on('libiconv')

    def configure_args(self):
        return [
            '--without-tar',
            '--with-libgpg-error-prefix=' + self.spec['libgpg-error'].prefix,
            '--with-libgcrypt-prefix='    + self.spec['libgcrypt'].prefix,
            '--with-libassuan-prefix='    + self.spec['libassuan'].prefix,
            '--with-ksba-prefix='         + self.spec['libksba'].prefix,
            '--with-npth-prefix='         + self.spec['npth'].prefix,
            '--without-ldap',
            '--with-libiconv-prefix='     + self.spec['libiconv'].prefix,
            '--without-regex',
            '--with-zlib='                + self.spec['zlib'].prefix,
            '--without-bzip2',
            '--without-readline',
        ]
