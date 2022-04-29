# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyExecuting(PythonPackage):
    """Get the currently executing AST node of a frame, and other information."""

    homepage = "https://github.com/alexmojaki/executing"
    pypi     = "executing/executing-0.8.2.tar.gz"

    version('0.8.2', sha256='c23bf42e9a7b9b212f185b1b2c3c91feb895963378887bb10e64a2e612ec0023')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm+toml', type='build')
