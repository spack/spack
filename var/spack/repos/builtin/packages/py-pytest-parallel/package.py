# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestParallel(PythonPackage):
    """A pytest plugin for parallel and concurrent testing."""

    homepage = "https://github.com/browsertron/pytest-parallel"
    pypi = "pytest-parallel/pytest-parallel-0.1.1.tar.gz"

    license("MIT")

    version(
        "0.1.1",
        sha256="9e3703015b0eda52be9e07d2ba3498f09340a56d5c79a39b50f22fc5c38212fe",
        url="https://pypi.org/packages/14/d2/a2cf7da29753a222d19a682d50fb3cb605544cec66770553611119c857d2/pytest_parallel-0.1.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pytest@3:")
        depends_on("py-tblib", when="@0.0.10:")
