# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfStandard(PythonPackage):
    """Standards document describing ASDF, Advanced Scientific Data Format"""

    homepage = "https://asdf-standard.readthedocs.io/"
    pypi = "asdf_standard/asdf_standard-1.0.3.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version(
        "1.0.3",
        sha256="1c628379c75f0663b6376a7e681d31b1b54391053e53447c9921fb04c26d41da",
        url="https://pypi.org/packages/b1/3e/2873079563324cbc60a152be07a38c8595bcfe0cadda4db8a1a1c9b5b2a7/asdf_standard-1.0.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.0.2:1.0")
        depends_on("py-importlib-resources@3:", when="@1.0.1:1.0 ^python@:3.8")
