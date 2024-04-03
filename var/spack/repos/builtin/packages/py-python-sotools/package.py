# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSotools(PythonPackage):
    """python-sotools is a collection of tools to work with ELF shared objects"""

    pypi = "python-sotools/python-sotools-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.0",
        sha256="19b9e89d9489d08063f008fb8a9c41114c1953b1df5dc81a6f456081596265a1",
        url="https://pypi.org/packages/0d/ec/e13991b717dea200e8e49a4b6d997bd901ea5619e747862499bcea3ec91d/python_sotools-0.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyelftools", when="@0.0.3:")
