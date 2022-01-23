# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cjson(CMakePackage):
    """Ultralightweight JSON parser in ANSI C."""

    homepage = 'https://github.com/DaveGamble/cJSON'
    git      = 'https://github.com/DaveGamble/cJSON'
    url      = 'https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.zip'

    version('1.7.15', sha256='c55519316d940757ef93a779f1db1ca809dbf979c551861f339d35aaea1c907c')
    version('1.7.14', sha256='d797b4440c91a19fa9c721d1f8bab21078624aa9555fc64c5c82e24aa2a08221')
    version('1.7.13', sha256='bef2d315985ca831f627a488ae0d568fb6e8416da918cd1d054424679bda79d8')
    version('1.7.12', sha256='532696aabfcb828a98670d1c7249066141fbc97cf45d3eae5a4c7c04a73fdbe7')
    version('1.7.11', sha256='84b248a7f0f625e50b358491fd6683d462eb8a3f5a64d7e75ad982d7b1720bbd')
    version('1.7.10', sha256='80a0584410656c8d8da2ba703744f44d7535fc4f0778d8bf4f980ce77c6a9f65')
    version('1.7.9',  sha256='24423b27417effc7355ccb737de6284beaf91f368ee2ce3d9041e93544d1c4a0')
    version('1.7.8',  sha256='5950bf4d88a16984794d6983d1e06e89537a310458fa2a73a008469836266dc6')
    version('1.7.7',  sha256='9494f0a9b2005f471c846fbdbb40a9de074ad5aee56e3e73518055cd639fa77e')
    version('1.7.6',  sha256='a8d79c49a06fc95c032dc1f82f1fa2fb5f6a3617b1700f793f915c5d550308c1')
    version('1.7.5',  sha256='e67fbbcd058da4f640b1920a9590c9aaec8f73ae098fcae9a718c87324bc95e4')
    version('1.7.4',  sha256='d1cb5cba69275b6a574f3b4fbc5ccdc066dd8bd89fb7ceca9a48a7929588bc6d')
    version('1.7.3',  sha256='1a5a836b8eb1cdb1a1c170338cc3ec0c9bfe6f493724abf07ae2d84438978a85')
    version('1.7.2',  sha256='8501399d508c76e08edf6cb62cd3b43be6d82e2ab234cef18891f9a91d43f612')
    version('1.7.1',  sha256='18778edc866a851736bfed189ac08f78f0abbbb47c03a727ac82ffa2ec69e670')
    version('1.7.0',  sha256='28ba437569c44c8b385e013bb4242596858c4db34f8bea22aeb573e0d484ac21')
    version('1.6.0',  sha256='a4151c81a67b9dabe55e547b0bef104dde5cf05aed801d236d95e8bb8b2e9796')
