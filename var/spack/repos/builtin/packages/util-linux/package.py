# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('2.29.2', '24e0c67aac6f5c2535208866a42aeea2')
    version('2.29.1', 'c7d5c111ef6bc5df65659e0b523ac9d9')
    version('2.25',   'f6d7fc6952ec69c4dc62c8d7c59c1d57')

    depends_on('python@2.7:')

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/util-linux/v{0}/util-linux-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec

        return [
            'PKG_CONFIG_PATH={0}'.format(
                join_path(spec['python'].prefix.lib, 'pkgconfig')),
            '--disable-use-tty-group',
        ]
