# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DeviceMapper(AutotoolsPackage):
    """The Device-mapper is a component of the linux kernel (since version
    2.6) that supports logical volume management.  This package provides
    the userspace configuration tools (dmsetup), library (libdevmapper) and
    header files. """

    homepage = "https://www.sourceware.org/dm"
    url      = "https://sourceware.org/pub/lvm2/releases/LVM2.2.03.05.tgz"

    version('2.2.03.05', sha256='ca52815c999b20c6d25e3192f142f081b93d01f07b9d787e99664b169dba2700')
    version('2.2.03.04', sha256='f151f36fc0039997d2d9369b607b9262568b1a268afe19fd1535807355402142')
    version('2.2.03.03', sha256='cedefa63ec5ae1b62fedbfddfc30706c095be0fc7c6aaed6fd1c50bc8c840dde')
    version('2.2.03.02', sha256='550ba750239fd75b7e52c9877565cabffef506bbf6d7f6f17b9700dee56c720f')
    version('2.2.03.01', sha256='424e58b074195ec08e0315fa1aff2550590998c33aea5c43bdceb8c1d135530b')
    version('2.2.03.00', sha256='405992bf76960e60c7219d84d5f1e22edc34422a1ea812e21b2ac3c813d0da4e')

    depends_on('libaio')

    def configure_args(self):
        return ['--enable-pkgconfig']

    def build(self, spec, prefix):
        make('device-mapper')

    def install(self, spec, prefix):
        make('install_device-mapper')
