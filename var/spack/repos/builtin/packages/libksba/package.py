# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libksba(AutotoolsPackage):
    """Libksba is a library to make the tasks of working with X.509
       certificates, CMS data and related objects more easy. """

    homepage = "https://gnupg.org/software/libksba/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libksba/libksba-1.3.5.tar.bz2"

    version('1.3.5', '8302a3e263a7c630aa7dea7d341f07a2')

    depends_on('libgpg-error')

    def configure_args(self):
        args = ['--with-libgpp-error=%s' % self.spec['libgpg-error'].prefix]
        return args
