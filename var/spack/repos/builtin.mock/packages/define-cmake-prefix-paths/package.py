# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DefineCmakePrefixPaths(Package):
    """Package that defines cmake_prefix_paths"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/definecmakeprefixpaths-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")

    @property
    def cmake_prefix_paths(self):
        paths = [self.prefix.test]
        return paths
