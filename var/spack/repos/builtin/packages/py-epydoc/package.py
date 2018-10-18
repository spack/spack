# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEpydoc(PythonPackage):
    """Epydoc is a tool for generating API documentation documentation for
       Python modules, based on their docstrings."""
    homepage = "https://pypi.python.org/pypi/epydoc"
    url      = "https://pypi.io/packages/source/e/epydoc/epydoc-3.0.1.tar.gz"

    version('3.0.1', '36407974bd5da2af00bf90ca27feeb44')
