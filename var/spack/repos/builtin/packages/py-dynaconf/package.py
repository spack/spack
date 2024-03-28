# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDynaconf(PythonPackage):
    """Dynaconf is a dynamic configuration management package for Python projects"""

    homepage = "https://github.com/dynaconf/dynaconf"
    pypi = "dynaconf/dynaconf-3.2.2.tar.gz"

    license("MIT")

    version(
        "3.2.2",
        sha256="0d62e51af6e9971e8e45cabee487ec70467d6c5065a9f070beac973bedaf1d54",
        url="https://pypi.org/packages/47/a6/154f6b6bbc7a2183d166fea2470caf8b904a38e2897852c5296f36aea3dd/dynaconf-3.2.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-python-dotenv", when="@0.5.4:2.2.1,2.2.3:3.0.0-rc1")
        depends_on("py-toml", when="@1:2.2.1,2.2.3:3.0.0-rc1")
