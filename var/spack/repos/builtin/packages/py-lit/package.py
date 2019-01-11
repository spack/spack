# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLit(PythonPackage):
    """lit is a portable tool for executing LLVM and Clang style test suites,
       summarizing their results, and providing indication of failures. lit is
       designed to be a lightweight testing tool with as simple a user
       interface as possible."""

    homepage = "https://pypi.python.org/pypi/lit"
    url      = "https://pypi.io/packages/source/l/lit/lit-0.5.0.tar.gz"

    version('0.5.0',  '8144660cc692be8fb903395a5f06564d')

    depends_on('py-setuptools', type='build')
