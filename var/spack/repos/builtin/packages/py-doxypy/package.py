# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDoxypy(PythonPackage):
    """doxypy is an input filter for Doxygen."""

    homepage = "https://pypi.python.org/pypi/doxypy"
    url      = "https://pypi.io/packages/source/d/doxypy/doxypy-0.3.tar.gz"

    version('0.3', '3b52289e0962d31b92af8be0eef8cbb2')

    depends_on('python@:2.8')
