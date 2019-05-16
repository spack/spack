# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGast(PythonPackage):
    """A generic AST to represent Python2 and Python3s Abstract Syntax Tree(AST)."""

    homepage = "https://pypi.org/project/gast/"
    url      = "https://files.pythonhosted.org/packages/5c/78/ff794fcae2ce8aa6323e789d1f8b3b7765f601e7702726f430e814822b96/gast-0.2.0.tar.gz"

    version('0.2.0', 'b58325eeafd44ddc761fe8904b6ca877')

    depends_on('py-setuptools', type='build')
