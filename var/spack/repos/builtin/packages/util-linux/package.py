# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UtilLinux(AutotoolsPackage):
    """Util-linux is a suite of essential utilities for any Linux system."""

    homepage = "http://freecode.com/projects/util-linux"
    url      = "https://www.kernel.org/pub/linux/utils/util-linux/v2.29/util-linux-2.29.2.tar.gz"
    list_url = "https://www.kernel.org/pub/linux/utils/util-linux"
    list_depth = 1

    version('2.29.2', sha256='29ccdf91d2c3245dc705f0ad3bf729ac41d8adcdbeff914e797c552ecb04a4c7')
    version('2.29.1', sha256='a6a7adba65a368e6dad9582d9fbedee43126d990df51266eaee089a73c893653')
    version('2.25',   sha256='7e43273a9e2ab99b5a54ac914fddf5d08ba7ab9b114c550e9f03474672bd23a1')

    depends_on('python@2.7:')
    depends_on('pkgconfig')

    # Make it possible to disable util-linux's libuuid so that you may
    # reliably depend_on(`libuuid`).
    variant('libuuid', default=True, description='Build libuuid')

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/util-linux/v{0}/util-linux-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        config_args = [
            '--disable-use-tty-group',
        ]
        config_args.extend(self.enable_or_disable('libuuid'))
        return config_args
