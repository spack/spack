# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutodocsumm(PythonPackage):
    """Extended sphinx autodoc including automatic autosummaries."""

    homepage = "https://github.com/Chilipp/autodocsumm"
    pypi = "autodocsumm/autodocsumm-0.2.11.tar.gz"

    maintainers("LydDeb")

    license("Apache-2.0")

    version(
        "0.2.11",
        sha256="f1d0a623bf1ad64d979a9e23fd360d1fb1b8f869beaf3197f711552cddc174e2",
        url="https://pypi.org/packages/c6/37/0a08e3e1d8b78185837c0c483267b87660ae74cdee0c91dc56ae83093965/autodocsumm-0.2.11-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2.9:")
        depends_on("py-sphinx@2.2:", when="@0.2.11:")
