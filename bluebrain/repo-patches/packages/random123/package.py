from spack import *
from spack.pkg.builtin.random123 import Random123 as BuiltinRandom123


class Random123(BuiltinRandom123):
    url      = "https://github.com/DEShawResearch/random123/archive/refs/tags/v1.14.0.tar.gz"

    version('1.14.0', sha256='effafd8656b18030b2a5b995cd3650c51a7c45052e6e1c21e48b9fa7a59d926e')
    version('1.13.2', sha256='74a1c6bb66b2684f03d3b1008642a2e9141909103cd09f428d2c60bcaa51cb40',
            url='https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.13.2.tar.gz')
    version('1.10', sha256='4afdfba4b941e33e23b5de9b7907b7e3ac326cb4d34b5fa8225edd00b5fe053b',
            url='https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.10.tar.gz')
    version('1.09', sha256='cf6abf623061bcf3d17e5e49bf3f3f0ae400ee89ae2e97c8cb8dcb918b1ebabe',
            url='https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.09.tar.gz')
