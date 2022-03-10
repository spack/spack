# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Expat(AutotoolsPackage):
    """Expat is an XML parser library written in C."""

    homepage = "https://libexpat.github.io/"
    url      = "https://github.com/libexpat/libexpat/releases/download/R_2_2_9/expat-2.2.9.tar.bz2"

    version('2.4.6', sha256='ce317706b07cae150f90cddd4253f5b4fba929607488af5ac47bf2bc08e31f09')
    # deprecate release 2.4.5 because of a regression
    version('2.4.5', sha256='fbb430f964c7a2db2626452b6769e6a8d5d23593a453ccbc21701b74deabedff', deprecated=True)
    # deprecate all releases before 2.4.5 because of security issues
    version('2.4.4', sha256='14c58c2a0b5b8b31836514dfab41bd191836db7aa7b84ae5c47bc0327a20d64a', deprecated=True)
    version('2.4.3', sha256='6f262e216a494fbf42d8c22bc841b3e117c21f2467a19dc4c27c991b5622f986', deprecated=True)
    version('2.4.1', sha256='2f9b6a580b94577b150a7d5617ad4643a4301a6616ff459307df3e225bcfbf40', deprecated=True)
    version('2.4.0', sha256='8c59142ef88913bc0a8b6e4c58970c034210ca552e6271f52f6cd6cce3708424', deprecated=True)
    version('2.3.0', sha256='f122a20eada303f904d5e0513326c5b821248f2d4d2afbf5c6f1339e511c0586', deprecated=True)
    version('2.2.10', sha256='b2c160f1b60e92da69de8e12333096aeb0c3bf692d41c60794de278af72135a5', deprecated=True)
    version('2.2.9', sha256='f1063084dc4302a427dabcca499c8312b3a32a29b7d2506653ecc8f950a9a237', deprecated=True)
    version('2.2.6', sha256='17b43c2716d521369f82fc2dc70f359860e90fa440bea65b3b85f0b246ea81f2', deprecated=True)
    version('2.2.5', sha256='d9dc32efba7e74f788fcc4f212a43216fc37cf5f23f4c2339664d473353aedf6', deprecated=True)
    version('2.2.2', sha256='4376911fcf81a23ebd821bbabc26fd933f3ac74833f74924342c29aad2c86046', deprecated=True)
    version('2.2.0', sha256='d9e50ff2d19b3538bd2127902a89987474e1a4db8e43a66a4d1a712ab9a504ff', deprecated=True)

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

    def url_for_version(self, version):
        url = 'https://github.com/libexpat/libexpat/releases/download/R_{0}/expat-{1}.tar.bz2'
        return url.format(version.underscored, version.dotted)

    def configure_args(self):
        spec = self.spec
        args = ['--without-docbook',
                '--enable-static',
                ]
        if '+libbsd' in spec and '@2.2.1:' in spec:
            args.append('--with-libbsd')
        return args
