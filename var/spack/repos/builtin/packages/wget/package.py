# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wget(AutotoolsPackage):
    """GNU Wget is a free software package for retrieving files using
    HTTP, HTTPS and FTP, the most widely-used Internet protocols. It is a
    non-interactive commandline tool, so it may easily be called from scripts,
    cron jobs, terminals without X-Windows support, etc."""

    homepage = "http://www.gnu.org/software/wget/"
    url      = "https://ftpmirror.gnu.org/wget/wget-1.19.1.tar.gz"

    version('1.19.1', '87cea36b7161fd43e3fd51a4e8b89689')
    version('1.17',   'c4c4727766f24ac716936275014a0536')
    version('1.16',   '293a37977c41b5522f781d3a3a078426')

    variant('ssl', default='openssl', values=('gnutls', 'openssl'),
            description='Specify SSL backend')
    variant('zlib', default=True,
            description='Enable zlib support')
    variant('libpsl', default=False,
            description='Enable support for libpsl cookie checking')
    variant('pcre', default=False,
            description='Enable PCRE style regular expressions')
    variant('python', default=False,
            description='Enable Python support')

    depends_on('gnutls',  when='ssl=gnutls')
    depends_on('openssl', when='ssl=openssl')

    depends_on('gettext', type='build')
    depends_on('python@3:', type='build', when='+python')

    depends_on('zlib', when='+zlib')
    depends_on('libpsl', when='+libpsl')
    depends_on('pcre', when='+pcre')

    depends_on('perl@5.12.0:', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('valgrind', type='test')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-ssl={0}'.format(spec.variants['ssl'].value),
        ]

        if '+zlib' in spec:
            args.append('--with-zlib')
        else:
            args.append('--without-zlib')

        if '+libpsl' in spec:
            args.append('--with-libpsl')
        else:
            args.append('--without-libpsl')

        if '+pcre' in spec:
            args.append('--enable-pcre')
        else:
            args.append('--disable-pcre')

        if self.run_tests:
            args.append('--enable-valgrind-tests')
        else:
            args.append('--disable-valgrind-tests')

        return args
