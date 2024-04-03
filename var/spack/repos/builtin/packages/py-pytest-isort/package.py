# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestIsort(PythonPackage):
    """py.test plugin to check import ordering using isort"""

    homepage = "https://github.com/moccu/pytest-isort/"
    pypi = "pytest-isort/pytest-isort-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.3.1",
        sha256="3be60e0de277b420ff89303ca6494320c41f7819ffa898756b90ef976e4c636a",
        url="https://pypi.org/packages/e4/01/94bdd1927582263947d37b2225412b9ef1763f8ebc9c42f55a650f718aca/pytest_isort-0.3.1-py2.py3-none-any.whl",
    )
