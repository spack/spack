# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCompressRawZlib(PerlPackage):
    """A low-Level Interface to zlib compression library."""

    homepage = "https://metacpan.org/pod/Compress::Raw::Zlib"
    url = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/Compress-Raw-Zlib-2.081.tar.gz"

    version("2.202", sha256="96e20946eb457a32d2d7a0050b922e37b5ada41246bcdc824196d3f7c4da91b7")
    version("2.201", sha256="a1413b20b17893e604251ca52f259c2554639531f4d82ff573137135b5137c06")
    version("2.200", sha256="99557fc5b4048ac97918064c172dd99c611c2caafe4c5b3181a23e039f7e4522")
    version("2.105", sha256="228159574899c56fe616c4dc889bddcf41db6079e095a2d622af96b043bbe7d8")
    version("2.104", sha256="5eb162c70ebe9bd3695f90361c4e11532875846e161ee48d2927d2f77dd5e08c")
    version("2.103", sha256="d69d2620ca024dc1b424f7f4228fe1169b2b77416bb30310e890d3be7da47dff")
    version("2.101", sha256="9d1b9515e8277c1b007e33fad1fd0f18717d56bf647e3794d61289c45b1aabb2")
    version("2.100", sha256="9fc6016cb2b07a1a41794f0c555e4449d16979716a8b4c704e86bbaaaa15992a")
    version("2.096", sha256="cd4cba20c159a7748b8bc91278524a7da70573d9531fde62298609a5f1c65912")
    version("2.095", sha256="ba2c653267d173834ea4d50827711e494ad6f7b7ea81a1859f53b260c6ad21b2")
    version("2.094", sha256="c0e4457b1e37a9cb724952d7ba8daa10d13293bd3eb3f6d6039367fbec5809e2")
    version("2.093", sha256="b5ec7194fa4a15738d3b8040ce42926342bb770e48d34a8d6008a1817e23e9f4")
    version("2.092", sha256="b0a25b8e49b40f84f79621ceefd132e700dc1730257822ce393afdf9a15c5b43")
    version("2.091", sha256="b67ffb902776367bcbbed1dca9495bac8844e5a9208566b7ce7c0afe65983f6f")
    version("2.090", sha256="f2c8499abcc7df90b8ccc3767b870cbd09d305b84b251a9573237ef2cf9eaf59")
    version("2.089", sha256="9ff8b0e8eb5568040cd5cc78eaccaac05cebaa756443201bb76663b40881f677")
    version("2.088", sha256="19a038b2dd8ffcc6e9bac45793e2258d5d80ed0286535851dd1b4af80b55023d")
    version("2.087", sha256="8c81c9e1e386b3620ea7aa4c393afe8c80d3587e4fde57b7f83106aea05bee8d")
    version("2.086", sha256="3f6dde715566b0cd8a41f6ae04f4da822614fe4a644c40b1a0e42293181f496d")
    version("2.084", sha256="355e197ba22e28de400e3b53ac8614327a2f7c8b8ca9276167c47439914a666f")
    version("2.083", sha256="5642998fe8c4a814326c10a97428335565525763761fe37f86e14a45a25c9e3e")
    version("2.081", sha256="e156de345bd224bbdabfcab0eeb3f678a3099a4e86c9d1b6771d880b55aa3a1b")

    depends_on("zlib")
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
