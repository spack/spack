# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfStandard(PythonPackage):
    """Standards document describing ASDF, Advanced Scientific Data Format"""

    homepage = "https://asdf-standard.readthedocs.io/"
    pypi = "asdf_standard/asdf_standard-1.0.3.tar.gz"

    maintainers("lgarrison")

    version("1.0.3", sha256="afd8ff9a70e7b17f6bcc64eb92a544867d5d4fe1f0076719142fdf62b96cfd44")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-importlib-resources@3:", type=("build", "run"), when="^python@:3.8")
