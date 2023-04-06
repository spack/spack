# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBasicNg(PythonPackage):
    """A modern skeleton for Sphinx themes."""

    homepage = "https://github.com/pradyunsg/sphinx-basic-ng"
    documentation = "https://rtfd.io/sphinx-basic-ng/"
    pypi = "sphinx_basic_ng/sphinx_basic_ng-0.0.1a12.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]
    version("0.0.1a12", sha256="cffffb14914ddd26c94b1330df1d72dab5a42e220aaeb5953076a40b9c50e801")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
