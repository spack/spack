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
    version('1.5.9',  sha256='77844680ffe4c29492ee59a215f850a66a04c69d514d3af5a6fcd7a49cc299ab')
    version('1.5.8',  sha256='cb673de9dd2af6efd03e2f9adab9bf0400c07a750bf94285d6e3439c8b2b92c0')
    version('1.5.7',  sha256='c23cfc870764c970ac70fcba93d87fc90f5fadc78d212d3a641ae8e9724d3dac')
    version('1.5.6',  sha256='ef5963df990a566055126a195490b56c37debc1a75ece1300702cd441b9e0cc2')
    version('1.5.5',  sha256='04217363f20218d324db2b6c6256f27ad35e3bae05be282ae5c1fd9d88e4ee32')
    version('1.5.4',  sha256='6ea1c004cf1eff760343681bc800852601f49ee8abd63cba338f1c3daea934b9')
    version('1.5.3',  sha256='3aafd00b92fb00b05ee18cbb4ec0dfb5801eb2293c620282c86bb60870bd32a9')
    version('1.5.2',  sha256='a77cc9742ee3742cd0c17dd8920bd66123a6484227ed2e8651608ee84e5a8c32')
    version('1.5.1',  sha256='48532a019db52b6f07c0ac8b926dbd3b0edf1e7fdb8e813afb67b3b24b93df02')
    version('1.5.0',  sha256='432790dc3e96ce6eadd1c6b9c616cd86bb040152a3a334b6764228c9252a710c')
    version('1.4.7',  sha256='02dba07f6bf1b5ac3ffe84ec8e123da7e73a8bf7b5c30331b3136413dd5faea0')
    version('1.4.6',  sha256='757f559f8ff78d3f6cc91f534b7eb68b9f4414259235127c31792e8368e2e546')
    version('1.4.5',  sha256='c4be3ef7062748b2bf3f1b45caa9024e9b7af6968658c19a1aa7b835fd9e7afb')
    version('1.4.4',  sha256='db888c8ae6641408c6e07e23e719ccbbb62818c65a75dffc076d9fceecbb8053')
    version('1.4.3',  sha256='d3dea85aad4cc443ad88801cb64dbb3c5a88b917a18d712ddded65e2982bd6ea')
    version('1.4.2',  sha256='6b77a16cf159098aa945e15d4c46058243d15c00506cb54c6cba2294cb338829')
    version('1.4.1',  sha256='b8d3215193e7c2df5c9ee12a18e5b09b2abe86e5cc78dd8721aed1aa1458063b')
    version('1.4.0',  sha256='56ff192cedf7575672152963689caf4f41d96bf2efb874e64ae5ad8a424a9398')
