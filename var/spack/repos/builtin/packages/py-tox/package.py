# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTox(PythonPackage):
    """tox is a generic virtualenv management and test command line tool."""

    homepage = "https://tox.readthedocs.org/"
    pypi = "tox/tox-3.14.2.tar.gz"

    license("MIT")

    version(
        "3.14.2",
        sha256="8dd653bf0c6716a435df363c853cad1f037f9d5fddd0abc90d0f48ad06f39d03",
        url="https://pypi.org/packages/a7/64/73ee95a48a69fb40f9ce415cdeda09c0c2721da483aae0687884f3cb0586/tox-3.14.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama@0.4.1:", when="@3.14.2:3 platform=windows")
        depends_on("py-filelock@3:", when="@:3.15.0")
        depends_on("py-importlib-metadata@1.1:1", when="@3.14.2 ^python@:3.7")
        depends_on("py-packaging", when="@3.13:3")
        depends_on("py-pluggy@0.12:0", when="@3.13:3.15.0")
        depends_on("py-py@1.4.17:", when="@:3.15.0")
        depends_on("py-six@1.0.0:", when="@:3.14.3")
        depends_on("py-toml@0.9.4:", when="@:3.25")
        depends_on("py-virtualenv@16:", when="@3.14.1:3.14.5")
