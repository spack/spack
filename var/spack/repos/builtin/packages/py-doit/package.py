# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDoit(PythonPackage):
    """doit - Automation Tool."""

    homepage = "http://pydoit.org/"
    pypi = "doit/doit-0.36.0.tar.gz"

    license("MIT")

    version(
        "0.36.0",
        sha256="ebc285f6666871b5300091c26eafdff3de968a6bd60ea35dd1e3fc6f2e32479a",
        url="https://pypi.org/packages/44/83/a2960d2c975836daa629a73995134fd86520c101412578c57da3d2aa71ee/doit-0.36.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.35:")
        depends_on("py-cloudpickle", when="@0.33:")
        depends_on("py-importlib-metadata@4.4:", when="@0.36:")
