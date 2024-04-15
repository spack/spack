# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEtelemetry(PythonPackage):
    """A lightweight python client to communicate with the etelemetry server"""

    homepage = "https://github.com/sensein/etelemetry-client"
    url = "https://github.com/sensein/etelemetry-client/archive/refs/tags/v0.2.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.0",
        sha256="78febd59a22eb53d052d731f10f24139eb2854fd237348fba683dd8616fb4a67",
        url="https://pypi.org/packages/8b/1b/a13fd41742cf2ed2498e90e5cdb27239e1115a788114aed0625dbf16737c/etelemetry-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="3e304ea9070902e6367282369cb8eaae05f4beef9313820053cc03f611bd1e29",
        url="https://pypi.org/packages/13/f9/e8e8cd04bdc44dfba28a3b2cc4d0b1efe8cbf3afc1bf12b11f1c9d697f1e/etelemetry-0.2.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.3:")
        depends_on("py-ci-info@0.2:", when="@0.2.1:")
        depends_on("py-requests")
