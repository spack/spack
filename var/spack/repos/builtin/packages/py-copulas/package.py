# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCopulas(PythonPackage):
    """Copulas is a Python library for modeling multivariate
    distributions and sampling from them using copula
    functions. Given a table containing numerical data, we can
    use Copulas to learn the distribution and later on generate
    new synthetic rows following the same statistical
    properties."""

    homepage = "https://github.com/sdv-dev/Copulas"
    pypi = "copulas/copulas-0.6.0.tar.gz"

    license("MIT")

    version(
        "0.6.0",
        sha256="556543df162dbd316aea5bffb0c17ed2c34f5b642abb52618a8e818260542872",
        url="https://pypi.org/packages/62/2a/9f801a73a61dedab6c34b9444b1710bc464f4ada8e85756de3599ad2cb51/copulas-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.11", when="@0.7.1:")
        depends_on("python@:3.9", when="@0.5.2.dev1:0.7.0")
        depends_on("python@:3.8", when="@0.3.2:0.5.2.dev0")
        depends_on("py-boto3@1.7.47:1.9", when="@0.2.3:0.3.0")
        depends_on("py-docutils@0.10:0.14", when="@0.2.3:0.3.0")
        depends_on("py-matplotlib@3.2.0:", when="@0.5:0.6.0")
        depends_on("py-numpy@1.20.0:1", when="@0.7.1: ^python@:3.9")
        depends_on("py-numpy@1.20.0:1", when="@0.5.2.dev1:0.7.0")
        depends_on("py-pandas@1.1.3:1", when="@0.7.1:0.8.0 ^python@:3.9")
        depends_on("py-pandas@1.1.3:1", when="@0.5.2.dev1:0.7.0")
        depends_on("py-scipy@1.5.4:", when="@0.7.1: ^python@:3.9")
        depends_on("py-scipy@1.5.4:", when="@0.5.2.dev1:0.7.0")
