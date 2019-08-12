# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minisign(CMakePackage):
    """Minisign is a dead simple tool to sign files and verify signatures."""

    homepage = "https://jedisct1.github.io/minisign/"
    url = "https://github.com/jedisct1/minisign/archive/0.7.tar.gz"

    version('0.7', 'd634202555c4f499e8ef9d6848d6f4ca')

    depends_on('libsodium')
