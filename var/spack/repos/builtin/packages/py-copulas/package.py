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
        "0.6.1",
        sha256="9db6686acb5101d1d615f6530ff59b094a8e7f053c9e073c64800a0be240e667",
        url="https://pypi.org/packages/03/8b/ec87edb5436a1b6a950c93732659209b7967b60189da69655d870930be13/copulas-0.6.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="556543df162dbd316aea5bffb0c17ed2c34f5b642abb52618a8e818260542872",
        url="https://pypi.org/packages/62/2a/9f801a73a61dedab6c34b9444b1710bc464f4ada8e85756de3599ad2cb51/copulas-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.5.2.dev1:0.7.0")
        depends_on("py-matplotlib@3.4.0:", when="@0.6.1:0.7.0 ^python@3.7:")
        depends_on("py-matplotlib@3.2.0:3.3", when="@0.6.1:0.7.0 ^python@:3.6")
        depends_on("py-matplotlib@3.2.0:", when="@0.5:0.6.0")
        depends_on("py-numpy@1.20.0:1", when="@0.5.2.dev1:0.7.0 ^python@3.7:")
        depends_on("py-numpy@1.18.0:1.19", when="@0.5.2.dev1:0.7.0 ^python@:3.6")
        depends_on("py-pandas@1.1.3:1", when="@0.5.2.dev1:0.7.0")
        depends_on("py-scipy@1.5.4:", when="@0.5.2.dev1:0.7.0")
