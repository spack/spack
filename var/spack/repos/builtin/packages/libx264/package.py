# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libx264(AutotoolsPackage):
    """x264 is a free software library and application for encoding video
    streams into the H.264/MPEG-4 AVC compression format."""

    homepage = "https://www.videolan.org/developers/x264.html"
    url      = "https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-20190811-2245.tar.bz2"

    version('264-snapshot-20190902-2245', sha256='413c0e9b59c1a47f51e3133ba10d4b665456a2687eee0b0a0add58c8684fdfd1')
    version('264-snapshot-20190901-2245', sha256='cac078c72a15ec8ae6883d3276e4921592606cbb271eb29c065eec91be21eed6')
    version('264-snapshot-20190831-2245', sha256='bf8f8eecc24e67d1986cfd5ddd6f862987354b5ffbf1cb0867f86a3c3c348783')

    depends_on('nasm')

    variant('shared', default=True, description='Enable shared libraries')

    def configure_args(self):
        config_args = ['--enable-static']
        config_args.extend(self.enable_or_disable('shared'))
        return config_args
