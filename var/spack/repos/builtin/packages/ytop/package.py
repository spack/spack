# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ytop(CargoPackage):
    """Another TUI based system monitor, this time in Rust!"""

    homepage  = "https://github.com/cjbassi/ytop"
    crates_io = "ytop"
    git       = "https://github.com/cjbassi/ytop"

    version('master', branch='master')
    version('0.6.2', sha256='16473b92b115c01faf8dd0b89fd12967684d3a88a5c6047d2f76b2dcfbcb0ed2')
    version('0.6.1', sha256='6f78a8c5809f9ce3a194b14f46fe67e0b4eace5c7633632345165ac082dbdef3')

    # Prior to 0.6.1, releases were only published to GitHub
    version(
        '0.6.0',
        url="https://github.com/cjbassi/ytop/archive/0.6.0.tar.gz",
        sha256='6ac47cf56b89d50689a85b38780463e99b1f3a4862a91657da410bce3acdcedb'
    )
    version(
        '0.5.1',
        url="https://github.com/cjbassi/ytop/archive/0.5.1.tar.gz",
        sha256='5eb8bc9fd210ac782ff51be98e387c9c63d69dfe97fa69f3fa11c58cf7c9d2df'
    )
    version(
        '0.5.0',
        url="https://github.com/cjbassi/ytop/archive/0.5.0.tar.gz",
        sha256='6c1ff6cfaa8072a9d6d984b38d8ebfaa042679dd1d63f2c300f68ad89039a341'
    )
    version(
        '0.4.3',
        url="https://github.com/cjbassi/ytop/archive/0.4.3.tar.gz",
        sha256='e46292f637ae5f11cfa2ce6f8a65a097317ae05d96aa34632f416878a921a41c'
    )
    version(
        '0.4.2',
        url="https://github.com/cjbassi/ytop/archive/0.4.2.tar.gz",
        sha256='2dc0c375e2f99fcdea1e38eb621e71dc5b65e2e67c4fd936c71c36bbe35ba489'
    )
    version(
        '0.4.1',
        url="https://github.com/cjbassi/ytop/archive/0.4.1.tar.gz",
        sha256='3c32d9b77f9e7301d123602f02a7205f315043bd393004e0827ce1c7424aedaa'
    )
    version(
        '0.4.0',
        url="https://github.com/cjbassi/ytop/archive/0.4.0.tar.gz",
        sha256='f35eec6158d677da636bc289fec266e15e35d43e364e5f7c461f16cc8ea89056'
    )
    version(
        '0.3.0',
        url="https://github.com/cjbassi/ytop/archive/0.3.0.tar.gz",
        sha256='61cfc8777f5924db035e9d1ce3a3cf222a7d894bef8e4723269bdb99b9ec2253'
    )
    version(
        '0.2.0',
        url="https://github.com/cjbassi/ytop/archive/0.2.0.tar.gz",
        sha256='6e39a1be2380b75d4a11be353bac131aa16e30455e681c3388a7d12baa2aee6f'
    )
    version(
        '0.1.0',
        url="https://github.com/cjbassi/ytop/archive/0.1.0.tar.gz",
        sha256='7831dffb9452a74b6d514fa6e639670745c8679d58b27a159f521478e0ae47d4'
    )
