# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Figcone(CMakePackage):
    """figcone - is a C++17 library, providing a convenient declarative interface for configuration
    parsers and built-in support for reading JSON, YAML, TOML, XML, INI and shoal config files."""

    homepage = "https://github.com/kamchatka-volcano/figcone"
    url = "https://github.com/kamchatka-volcano/figcone/archive/refs/tags/v2.4.9.tar.gz"

    version("2.4.9", sha256="735399e849621a4923e71a50d5e2ba928d5dfa3b01e54d56e0bac8e5102b7697")
    version("2.4.8", sha256="55922b27900524ab3fa4fc996bcf5459c89ee083671fa2f8f7d99a7c47113f80")
    version("2.4.7", sha256="75d84edbcf8aeb838245c8ea2188c969cceac5d6290e993291caa711fee3cdca")
    version("2.4.5", sha256="d842bc5d6c6222bed98d8192d4075487df4f499827a2288459b559818377b431")
    version("2.4.3", sha256="86816620f09ef57eb226f7a31521a4e48bcddedf04110c7bc95a164852954912")
    version("2.4.2", sha256="326e999458b1b8e8f46da1e7d23e7ab11014af9bf83244ee5926ce8c534e1567")
    version("2.4.1", sha256="93380e9ca8ef1ec2a66b1b23c9ff2048572518291e11bc8929345a7fd155a6ed")
    version("2.4.0", sha256="640f2dfb417f0d7fb5fa44c4d469ac95011bbf382635d114315fd11917e931e1")
    version("2.3.0", sha256="07e444901ee6b0d9b8033184467e8da7e5cbcf2665724b119fe2ba5ef1bee6a9")
