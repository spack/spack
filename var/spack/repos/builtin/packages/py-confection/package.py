# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfection(PythonPackage):
    """The sweetest config system for Python"""

    homepage = "https://github.com/explosion/confection"
    pypi = "confection/confection-0.0.4.tar.gz"

    license("MIT")

    version(
        "0.0.4",
        sha256="aeac5919ba770c7b281aa5863bb6b0efed42568a7ad8ea26b6cb632154503fb2",
        url="https://pypi.org/packages/b1/c4/07291f4947d20f545eee76ef20d1eacfb1f80d1d6ab4792bfa6797e0578c/confection-0.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pydantic@1.7.4:1.7,1.8.2:1", when="@0.0.3:0.1.0")
        depends_on("py-srsly@2.4:2.4.0.0,2.4.1:", when="@0.0.1:")
        depends_on("py-typing-extensions@3.7.4.1:4.4", when="@0.0.4: ^python@:3.7")
