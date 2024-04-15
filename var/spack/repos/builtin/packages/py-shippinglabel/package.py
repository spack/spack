# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyShippinglabel(PythonPackage):
    """Utilities for handling packages."""

    homepage = "https://github.com/domdfcoding/shippinglabel"
    pypi = "shippinglabel/shippinglabel-1.5.0.tar.gz"

    license("MIT")

    version(
        "1.5.0",
        sha256="5d4fed80499c00250d5e660296e7d6d0607ee4f2543b2d4bca72958f2b710241",
        url="https://pypi.org/packages/07/86/cc4be0164a335dea582be2bfb3d72fdacfbfa534b9791c580a3f5f5b3768/shippinglabel-1.5.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-apeye@1:", when="@1:")
        depends_on("py-dist-meta@0.1.2:", when="@1:")
        depends_on("py-dom-toml@0.2.2:")
        depends_on("py-domdf-python-tools@3.1:", when="@1:")
        depends_on("py-packaging@20.9:")
        depends_on("py-platformdirs@2.3:", when="@1.2:")
        depends_on("py-typing-extensions@3.7.4.3:")

    conflicts("^py-setuptools@61")
