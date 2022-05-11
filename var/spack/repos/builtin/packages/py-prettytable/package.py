# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPrettytable(PythonPackage):
    """PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually
    appealing ASCII tables.
    """

    homepage = "https://github.com/jazzband/prettytable"
    pypi = "prettytable/prettytable-0.7.2.tar.gz"

    version('3.2.0', sha256='ae7d96c64100543dc61662b40a28f3b03c0f94a503ed121c6fca2782c5816f81')
    version('2.4.0', sha256='18e56447f636b447096977d468849c1e2d3cfa0af8e7b5acfcf83a64790c0aca')
    version('0.7.2', sha256='2d5460dc9db74a32bcc8f9f67de68b2c4f4d2f01fa3bd518764c69156d9cacd9')

    depends_on("py-setuptools", type='build')
    depends_on("py-wcwidth", type=('build', 'run'), when='@2.4.0:')
    depends_on("py-importlib-metadata", type=('build', 'run'), when='@2.4.0: ^python@:3.7')
    depends_on("py-setuptools-scm", type='build', when='@2.4.0:')
    depends_on("python@3.6:", type=('build', 'run'), when='@2.4.0:')
    depends_on("python@3.7:", type=('build', 'run'), when='@3.2.0:')
