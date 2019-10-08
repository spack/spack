# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tar(AutotoolsPackage):
    """GNU Tar provides the ability to create tar archives, as well as various
    other kinds of manipulation."""

    homepage = "https://www.gnu.org/software/tar/"
    url      = "https://ftpmirror.gnu.org/tar/tar-1.32.tar.gz"

    version('1.32', sha256='b59549594d91d84ee00c99cf2541a3330fed3a42c440503326dab767f2fbb96c')
    version('1.31', sha256='b471be6cb68fd13c4878297d856aebd50551646f4e3074906b1a74549c40d5a2')
    version('1.30', 'e0c5ed59e4dd33d765d6c90caadd3c73')
    version('1.29', sha256='cae466e6e58c7292355e7080248f244db3a4cf755f33f4fa25ca7f9a7ed09af0')
    version('1.28', '6ea3dbea1f2b0409b234048e021a9fd7')

    depends_on('libiconv')

    patch('tar-pgi.patch',    when='@1.29')
    patch('config-pgi.patch', when='@:1.29')
    patch('se-selinux.patch', when='@:1.29')
    patch('argp-pgi.patch',   when='@:1.29')
    patch('gnutar-configure-xattrs.patch', when='@1.28')

    def configure_args(self):
        return [
            '--with-libiconv-prefix={0}'.format(self.spec['libiconv'].prefix),
        ]
