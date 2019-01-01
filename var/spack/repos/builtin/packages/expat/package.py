# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Expat(AutotoolsPackage):
    """Expat is an XML parser library written in C."""

    homepage = "https://libexpat.github.io/"
    url      = "https://github.com/libexpat/libexpat/releases/download/R_2_2_2/expat-2.2.2.tar.bz2"

    # Version 2.2.2 introduced a requirement for a high quality
    # entropy source.  "Older" linux systems (aka CentOS 7) do not
    # support get_random so we'll provide a high quality source via
    # libbsd.
    # There's no need for it in earlier versions, so 'conflict' if
    # someone's asking for an older version and also libbsd.
    # In order to install an older version, you'll need to add
    # `~libbsd`.
    variant('libbsd', default=sys.platform != 'darwin',
            description="Use libbsd (for high quality randomness)")
    depends_on('libbsd', when="@2.2.1:+libbsd")

    version('2.2.5', '789e297f547980fc9ecc036f9a070d49')
    version('2.2.2', '1ede9a41223c78528b8c5d23e69a2667')
    version('2.2.0', '2f47841c829facb346eb6e3fab5212e2')

    def url_for_version(self, version):
        url = 'https://github.com/libexpat/libexpat/releases/download/R_{0}/expat-{1}.tar.bz2'
        return url.format(version.underscored, version.dotted)

    def configure_args(self):
        spec = self.spec
        args = []
        if '+libbsd' in spec and '@2.2.1:' in spec:
            args = ['--with-libbsd']
        return args
