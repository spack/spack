# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySdv(PythonPackage):
    """The Synthetic Data Vault (SDV) is a Synthetic Data
    Generation ecosystem of libraries that allows users to
    easily learn single-table, multi-table and timeseries
    datasets to later on generate new Synthetic Data that
    has the same format and statistical properties as the
    original dataset."""

    maintainers("Kerilk", "jke513")

    homepage = "https://github.com/sdv-dev/SDV"
    pypi = "sdv/sdv-0.13.1.tar.gz"

    license("MIT")

    version(
        "0.14.0",
        sha256="e9f3e28b913e2723accb2c109fc95be6b7ffc50f0365c8699cd7e5a9cad79c38",
        url="https://pypi.org/packages/47/9b/4444f38c9b4d1c8e906660319cc52c3de84bebc5c8e8ff593a2794363711/sdv-0.14.0-py2.py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="b5a0b8826d2f1bf624292afade09a4815726ef568da49e001ca10bcde62f826a",
        url="https://pypi.org/packages/f6/4b/247fccbeff223ed4ac0261ddfca43ccded520701752f1d7398b286b9f97a/sdv-0.13.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.13:0.17")
        depends_on("py-copulas@0.6.1:0.6.1.0", when="@0.14,0.15.0.dev:0.15.0.dev0")
        depends_on("py-copulas@0.6:0.6.0.0,0.6.1:0.6", when="@0.13")
        depends_on("py-ctgan@0.5.1:0.5.1.0,0.5.2:0.5", when="@0.14:0.16")
        depends_on("py-ctgan@0.5:0.5.0.0,0.5.1:0.5", when="@0.13")
        depends_on("py-deepecho@0.3.0.post:0.3", when="@0.13:0.17")
        depends_on("py-faker@3:9", when="@0.13:0.16,0.17.0.dev:0.17.0.dev0")
        depends_on("py-graphviz@0.13.2:")
        depends_on("py-numpy@1.20.0:1", when="@0.13:0.17 ^python@3.7:")
        depends_on("py-numpy@1.18.0:1.19", when="@0.13:0.17 ^python@:3.6")
        depends_on("py-pandas@1.1.3:1", when="@0.13:0.17")
        depends_on("py-rdt@0.6.2:0.6.2.0,0.6.3:0", when="@0.14:0.16")
        depends_on("py-rdt@0.6.1:0.6.1.0,0.6.2:0", when="@0.13")
        depends_on(
            "py-sdmetrics@0.4.1:0.4.1.0,0.4.2:0.4", when="@0.13.1:0.14,0.15.0.dev:0.15.0.dev0"
        )
        depends_on("py-tqdm@4.15:", when="@0.13:")
