# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rdkit(CMakePackage):
    """RDKit is a collection of cheminformatics and machine-learning
       software written in C++ and Python."""

    homepage = "https://www.rdkit.org"
    url      = "https://github.com/rdkit/rdkit/archive/refs/tags/Release_2021_03_2.tar.gz"

    maintainers = ['bvanessen']

    version('2021_03_2',   sha256='9907a745405cc915c65504046e446199f8ad03d870714de57c27d3738f330fe4')
    version('2021_03_1b1', sha256='2cd0673b289ba756c76a1bf57cf19e147ac4a9f6ecf9e79cc3dd86c8d39be414')
    version('2021_03_1',   sha256='9495f797a54ac70b3b6e12776de7d82acd7f7b5d5f0cc1f168c763215545610b')
    version('2020_09_5',   sha256='85cec9618e7ef6365b9b908ed674c073d898b6627521cc7fd8c2e05fea8a5def')
    version('2020_09_4',   sha256='9e734ca8f99d8be1ef2ac51efb67c393c62e88b98cfa550d6173ce3eaa87b559')
    version('2020_09_3',   sha256='aa95bf3cbeef287eeb6d9759ff0992d2f92f2171b1758af71b7c9a0ec97a0660')
    version('2020_09_2',   sha256='44663970859c0ec993f94a56b692231557df02c267853a2ee3c1f609cef93ae9')
    version('2020_09_1b1', sha256='d9d836dc38cc45db44698e33325901452c94df9add10dd2675674594af1b73c2')
    version('2020_09_1',   sha256='ac105498be52ff77f7e9328c41d0e61a2318cac0789d6efc30f5f50dc78a992c')
    version('2020_03_6',   sha256='a3663295a149aa0307ace6d1995094d0334180bc8f892fa325558a110154272b')

    depends_on('python@3:')
    depends_on('boost@1.53.0: +python +serialization')

    depends_on('py-numpy')
    depends_on('sqlite')

    extends("python")

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD=14',
                '-DRDK_INSTALL_INTREE=OFF']
        return args
