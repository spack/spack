# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cmaketools(MakefilePackage):
    """This is a small package containing some commonly used CMake "find" modules.

       To use them, you need to have the top directory in the CMAKE_PREFIX_PATH, then you can enable the modules in your CMakeLists.txt with something like:

       find_package(CMakeTools)
       UseCMakeTools()
    """

    homepage = "https://github.com/HSF/cmaketools"
    url      = "https://github.com/HSF/cmaketools/archive/1.8.tar.gz"

    version('1.8', sha256='91af30f5701dadf80a5d7e0d808c224c934f0784a3aff2d3b69aff24f7e1db41')
    version('1.7', sha256='233138af36cfbb17f60285274157d189485c3918d44d5303d21823e4d0875c3f')
    version('1.6', sha256='7d2a3f57ad6c20dca2a1ce7174f68aca88edc3861f67c41283c82b5e24660192')
    version('1.5', sha256='e1ca392a3d8471b31049b8f0a6d9ff341ad88ef0e05ebc99d490c634cf8f69bd')
    version('1.4', sha256='edbdd4188823247fc80a51f1686b19ffa031c4e6401763c338c0f184d71d5511')
    version('1.3', sha256='56b983467d7a49704e7540c110c2944a5b5aaab27aaedac8f9c0817c62608b3e')
    version('1.2', sha256='7ebea2cf6a4db725bde8193070dc530afc410a294d5d531d0d8b0de237d6335c')
    version('1.1', sha256='3a0f430e70bf47956d34bc06e5b8bb5943a74d0dc9d74c3e7218fa6d4ee7ccd9')
    version('1.0', sha256='b6098962737c86b60046edaa780dc16e29a70ee1edce979062acaf93bda6a47f')

    def install(self, spec, prefix):
        install_tree('.', prefix)