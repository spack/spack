# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Iwyu(CMakePackage):
    """include-what-you-use: A tool for use with clang to analyze #includes in
    C and C++ source files
    """

    homepage = "https://include-what-you-use.org"
    url      = "https://include-what-you-use.org/downloads/include-what-you-use-0.13.src.tar.gz"

    maintainers = ['sethrj']

    version('0.13', sha256='49294270aa64e8c04182369212cd919f3b3e0e47601b1f935f038c761c265bc9')
    version('0.12', sha256='a5892fb0abccb820c394e4e245c00ef30fc94e4ae58a048b23f94047c0816025')
    version('0.11', sha256='2d2877726c4aed9518cbb37673ffbc2b7da9c239bf8fe29432da35c1c0ec367a')

    patch('iwyu-013-cmake.patch', when='@0.13')

    depends_on('llvm+clang@9.0:9.999', when='@0.13')
    depends_on('llvm+clang@8.0:8.999', when='@0.12')
    depends_on('llvm+clang@7.0:7.999', when='@0.11')
