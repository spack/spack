# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPep8(PythonPackage):
    """Python style guide checker (deprecated, use py-pycodestyle instead)."""

    homepage = "https://pep8.readthedocs.org/"
    pypi = "pep8/pep8-1.7.1.tar.gz"

    version(
        "1.7.1",
        sha256="b22cfae5db09833bb9bd7c8463b53e1a9c9b39f12e304a8d0bba729c501827ee",
        url="https://pypi.org/packages/42/3f/669429ce58de2c22d8d2c542752e137ec4b9885fff398d3eceb1a7f5acb4/pep8-1.7.1-py2.py3-none-any.whl",
    )
