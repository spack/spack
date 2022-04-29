# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Cli11(CMakePackage):
    """CLI11 is a command line parser for C++11 and beyond that provides a rich
    feature set with a simple and intuitive interface."""

    homepage = "https://cliutils.github.io/CLI11/book/"
    url      = "https://github.com/CLIUtils/CLI11/archive/v1.9.1.tar.gz"
    maintainers = ['nightlark']

    version('2.1.1', sha256='d69023d1d0ab6a22be86b4f59d449422bc5efd9121868f4e284d6042e52f682e')
    version('2.1.0', sha256='2661b0112b02478bad3dc7f1749c4825bfc7e37b440cbb4c8c0e2ffaa3999112')
    version('2.0.0', sha256='2c672f17bf56e8e6223a3bfb74055a946fa7b1ff376510371902adb9cb0ab6a3')
    version('1.9.1', sha256='c780cf8cf3ba5ec2648a7eeb20a47e274493258f38a9b417628e0576f473a50b')

    depends_on('cmake@3.4:', type='build')

    def cmake_args(self):
        args = [
            '-DCLI11_BUILD_EXAMPLES=OFF',
            '-DCLI11_BUILD_DOCS=OFF',
            '-DCLI11_BUILD_TESTS=OFF',
        ]
        return args
