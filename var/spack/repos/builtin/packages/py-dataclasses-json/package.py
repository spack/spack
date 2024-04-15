# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataclassesJson(PythonPackage):
    """Easily serialize dataclasses to and from JSON."""

    homepage = "https://github.com/lidatong/dataclasses-json"
    pypi = "dataclasses_json/dataclasses_json-0.5.12.tar.gz"

    license("MIT")

    version(
        "0.5.12",
        sha256="ece0f002af8d7b19c757c62b82ffb414e4bf49e856471f4070ba06590150c345",
        url="https://pypi.org/packages/26/3a/502d66312c1e707a4d5f73d2fc2165a4217d8c77df3a1eb4c09db26dd3b0/dataclasses_json-0.5.12-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3.11", when="@0.5.12:0.5.13")
        depends_on("py-marshmallow@3.18:", when="@0.5.12:")
        depends_on("py-typing-inspect@0.4:", when="@0.5.12:")
