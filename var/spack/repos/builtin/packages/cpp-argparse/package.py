# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CppArgparse(CMakePackage):
    """Argument Parser for Modern C++"""

    homepage = "https://github.com/p-ranav/argparse/"
    url = "https://github.com/p-ranav/argparse/archive/refs/tags/v2.2.tar.gz"

    maintainers("qoelet")

    version("2.9", sha256="cd563293580b9dc592254df35b49cf8a19b4870ff5f611c7584cf967d9e6031e")
    version("2.2", sha256="f0fc6ab7e70ac24856c160f44ebb0dd79dc1f7f4a614ee2810d42bb73799872b")
