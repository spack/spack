# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Krb5(AutotoolsPackage):
    """Network authentication protocol"""

    homepage = "https://kerberos.org"
    url      = "https://kerberos.org/dist/krb5/1.16/krb5-1.16.1.tar.gz"

    version('1.16.1', sha256='214ffe394e3ad0c730564074ec44f1da119159d94281bbec541dc29168d21117')

    depends_on('bison', type='build')
    depends_on('openssl')

    configure_directory = 'src'
    build_directory = 'src'

    def configure_args(self):
        args = ['--disable-debug',
                '--disable-dependency-tracking',
                '--disable-silent-rules',
                '--without-system-verto']
        return args
