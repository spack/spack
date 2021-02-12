# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDbFile(PerlPackage):
    """DB_File is a module which allows Perl programs to make use of the
    facilities provided by Berkeley DB version 1.x (if you have a newer version
    of DB, see "Using DB_File with Berkeley DB version 2 or greater").
    It is assumed that you have a copy of the Berkeley DB manual pages at hand
    when reading this documentation. The interface defined here mirrors the
    Berkeley DB interface closely."""

    homepage = "https://metacpan.org/pod/DB_File"
    url      = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/DB_File-1.840.tar.gz"

    version('1.855', sha256='d9ffe2a25be6cdfee7a34d64235cdc899e99ba8b3fb8de8a9e7f4af20e4ca960')
    version('1.854', sha256='bec4961c558969c88e170c35a25d290d822355b690331ea0c9db5455bc55603b')
    version('1.853', sha256='d0c859cdb006c86d97b6dc316cb64b42b5b4178bd0c270e3d440ee42a23e26f9')
    version('1.852', sha256='3ab7957523b6da39c55cb2ec4e677d88aa4034fd0b2f40788781a58e7d078391')
    version('1.851', sha256='68b7094e506a5b1673b7ec47ad2dfd66d1a28f20be8e657beb9ddbf06c3547c8')
    version('1.850', sha256='f6f35774f3f50df331de8a07d34590fa29e677a31691004e9e569dcb27e245ee')
    version('1.843', sha256='de24e3d1e56b1b56c1f143590fb8ab8b812ebd9697e9c01349b0ba11c36f346a')
    version('1.842', sha256='0f163850d81c51461994079411ac32fe3707d91befbae4c4b359e1a4774a4d70')
    version('1.841', sha256='169ab1e33eb48d2c451db0d4c3cd7e049f9a676294f45e818a97e93705d1d385')
    version('1.840', sha256='b7864707fad0f2d1488c748c4fa08f1fb8bcfd3da247c36909fd42f20bfab2c4')

    depends_on('perl-extutils-makemaker', type='build')
    depends_on('berkeley-db', type='build')

    def patch(self):
        filter_file('/usr/local/BerkeleyDB',
                    self.spec['berkeley-db'].prefix, 'config.in')
