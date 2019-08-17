# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyelftools(PythonPackage):
    """A pure-Python library for parsing and analyzing ELF files and DWARF
       debugging information"""
    homepage = "https://pypi.python.org/pypi/pyelftools"
    url      = "https://pypi.io/packages/source/p/pyelftools/pyelftools-0.23.tar.gz"

    version('0.23', 'aa7cefa8bd2f63d7b017440c9084f310')
