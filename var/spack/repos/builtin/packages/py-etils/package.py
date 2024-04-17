# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEtils(PythonPackage):
    """etils (eclectic utils) is an open-source collection of utils
    for python."""

    homepage = "https://github.com/google/etils"
    pypi = "etils/etils-0.9.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.7.0",
        sha256="61af8f7c242171de15e22e5da02d527cb9e677d11f8bcafe18fcc3548eee3e60",
        url="https://pypi.org/packages/37/10/dd5b124f037a636783e416a2fe839edd7ec63c0dce7ce4f3c1da029aeb80/etils-1.7.0-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="635d6f7d1c519eb194304228543a4c5c7df0e6b58243302473e34c18cf720588",
        url="https://pypi.org/packages/76/ac/4f4b4096acd0160e0895715b47974b1f304b5e4a6b5169ce8d1355820eb4/etils-0.9.0-py3-none-any.whl",
    )

    variant("epath", default=False, description="with epath module")
    variant("epy", default=False, description="with epy module")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@1.6:1.7")
        depends_on("python@3.7:", when="@:0")
        depends_on("py-fsspec", when="@1.5:+epath")
        depends_on("py-importlib-resources", when="@0.6:+epath")
        depends_on("py-typing-extensions", when="@0.7:+epath")
        depends_on("py-typing-extensions", when="@0.5:+epy")
        depends_on("py-zipp", when="@0.6:+epath")

    conflicts("~epy", when="+epath")
