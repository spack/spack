# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibgpgError(AutotoolsPackage):
    """Libgpg-error is a small library that defines common error
       values for all GnuPG components. Among these are GPG, GPGSM,
       GPGME, GPG-Agent, libgcrypt, Libksba, DirMngr, Pinentry,
       SmartCard Daemon and possibly more in the future. """

    homepage = "https://www.gnupg.org/related_software/libgpg-error"
    url = "https://gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.27.tar.bz2"

    version('1.36', sha256='babd98437208c163175c29453f8681094bcaf92968a15cafb1a276076b33c97c')
    version('1.27', '5217ef3e76a7275a2a3b569a12ddc989')
    version('1.21', 'ab0b5aba6d0a185b41d07bda804fd8b2')
    version('1.18', '12312802d2065774b787cbfc22cc04e9')
