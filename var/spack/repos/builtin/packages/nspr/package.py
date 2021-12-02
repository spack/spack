# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nspr(AutotoolsPackage):
    """Netscape Portable Runtime (NSPR) provides a platform-neutral API
    for system level and libc-like functions."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Reference/NSPR_functions"
    url      = "https://ftp.mozilla.org/pub/nspr/releases/v4.13.1/src/nspr-4.13.1.tar.gz"

    version('4.31',   sha256='5729da87d5fbf1584b72840751e0c6f329b5d541850cacd1b61652c95015abc8')
    version('4.13.1', sha256='5e4c1751339a76e7c772c0c04747488d7f8c98980b434dc846977e43117833ab')

    depends_on('perl', type='build')

    configure_directory = 'nspr'

    def configure_args(self):
        return [
            '--with-mozilla',
            '--enable-64bit',  # without this, fails when 32-bit glibc not found
            '--enable-optimize',
        ]

    @property
    def headers(self):
        headers = find_headers('*', self.prefix.include, recursive=True)
        headers.directories = [self.prefix.include.nspr]
        return headers
