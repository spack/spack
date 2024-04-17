# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDict2css(PythonPackage):
    """A μ-library for constructing cascading style sheets from Python dictionaries."""

    homepage = "https://github.com/sphinx-toolbox/dict2css"
    pypi = "dict2css/dict2css-0.3.0.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "0.3.0",
        sha256="ef934ce73a225fdd5f811b484fe9e2dd768f7ef14a89fc8f4eb5672597131d00",
        url="https://pypi.org/packages/ff/1c/5c108f07fc0818bef046fd1d6cdd84ba081833d59b1adbc3a112a0f741cd/dict2css-0.3.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-cssutils@2.2:", when="@0.3:")
        depends_on("py-domdf-python-tools@2.2:")
