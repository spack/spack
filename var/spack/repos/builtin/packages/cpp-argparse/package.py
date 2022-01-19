# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CppArgparse(CMakePackage):
    """Argument Parser for Modern C++"""
    homepage = "https://github.com/p-ranav/argparse/"
    url      = "https://github.com/p-ranav/argparse/archive/refs/tags/v2.2.tar.gz"

    maintainers = ['qoelet']

    version('2.2', sha256='f0fc6ab7e70ac24856c160f44ebb0dd79dc1f7f4a614ee2810d42bb73799872b')
