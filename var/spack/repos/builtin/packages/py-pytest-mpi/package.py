# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPytestMpi(PythonPackage):
    """Pytest plugin to collect information from tests."""

    homepage = "https://pytest-mpi.readthedocs.io"
    pypi = "pytest-mpi/pytest-mpi-0.6.tar.gz"

    license("BSD-3-Clause")

    maintainers("tristan0x")

    version(
        "0.6",
        sha256="1b7e193fb3be31d08c8e4dd7435e8e13e14b17ead6a6fc6aa07a6d3c7145590b",
        url="https://pypi.org/packages/a6/2b/0ed49de84e96ebf771c86a16d88b48c08d291627cfcdce30973f8538c99e/pytest_mpi-0.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pytest", when="@0.5-alpha1:")
