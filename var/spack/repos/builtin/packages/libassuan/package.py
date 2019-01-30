# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libassuan(AutotoolsPackage):
    """Libassuan is a small library implementing the so-called Assuan
       protocol."""

    homepage = "https://gnupg.org/software/libassuan/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libassuan/libassuan-2.4.5.tar.bz2"

    version('2.4.5', '4f22bdb70d424cfb41b64fd73b7e1e45')
    version('2.4.3', '8e01a7c72d3e5d154481230668e6eb5a')

    depends_on('libgpg-error')

    def configure_args(self):
        args = ['--with-libgpp-error=%s' % self.spec['libgpg-error'].prefix]
        return args
