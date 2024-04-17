# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConsolekit(PythonPackage):
    """Additional utilities for click."""

    homepage = "https://github.com/domdfcoding/consolekit"
    pypi = "consolekit/consolekit-1.5.1.tar.gz"

    license("MIT")

    version(
        "1.5.1",
        sha256="5f9f98b2d618d51cd9ddb73062c531811253d144b05ae351a972867b4ecde7b9",
        url="https://pypi.org/packages/3e/86/93eb5e2bd7b05cb04cf555da79c4bb769c5d0966c5592831273b570e4129/consolekit-1.5.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click@7.1.2:")
        depends_on("py-colorama@0.4.3:", when="platform=windows ^python@:3.9")
        depends_on("py-deprecation-alias@0.1.1:")
        depends_on("py-domdf-python-tools@2.6:", when="@1.2.2:1.5")
        depends_on("py-mistletoe@0.7.2:")
        depends_on("py-typing-extensions@3.10:3.10.0.0,3.10.0.2:", when="@1.3.2:")

    conflicts("^py-typing-extensions@3.10.0.1")
