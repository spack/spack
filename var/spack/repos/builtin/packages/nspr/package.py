# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nspr(AutotoolsPackage):
    """Netscape Portable Runtime (NSPR) provides a platform-neutral API
    for system level and libc-like functions."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSPR"

    version('4.13.1',
            url = 'http://ftp.mozilla.org/pub/nspr/releases/v4.13.1/src/nspr-4.13.1.tar.gz',
            sha256='5e4c1751339a76e7c772c0c04747488d7f8c98980b434dc846977e43117833ab')
    version('4.22',
            url = 'https://ftp.mozilla.org/pub/nspr/releases/v4.22/src/nspr-4.22.tar.gz',
            sha256='c9e4b6cc24856ec93202fe13704b38b38ba219f0f2aeac93090ce2b6c696d430')

    depends_on('perl', type='build')

    configure_directory = 'nspr'

    def configure_args(self):
        return [
            '--with-mozilla',
            '--enable-64bit'  # without this, fails when 32-bit glibc not found
        ]
