# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySdmetrics(PythonPackage):
    """The SDMetrics library provides a set of dataset-agnostic
    tools for evaluating the quality of a synthetic database
    by comparing it to the real database that it is modeled
    after."""

    maintainers("Kerilk", "jke513")

    homepage = "https://github.com/sdv-dev/SDMetrics"
    pypi = "sdmetrics/sdmetrics-0.4.1.tar.gz"

    license("MIT")

    version(
        "0.4.1",
        sha256="479ab86f466e69e12edf6d707a892479a939eb9e42ffb2b7dc6afdfddb998ee9",
        url="https://pypi.org/packages/f6/72/8f85dfbd06466ff64d03d4fddb2874c2c0d9ea1bba34f305ab4588135dfd/sdmetrics-0.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.4:0.8")
        depends_on("py-copulas@0.6:0.6.0.0,0.6.1:0.6", when="@0.4:0.4.1")
        depends_on("py-numpy@1.18.0:1.19", when="@0.4:0.8 ^python@:3.6")
        depends_on("py-numpy@1.20.0:1", when="@0.4:0.8 ^python@3.7:")
        depends_on("py-pandas@1.1.3:1", when="@0.4:0.8")
        depends_on("py-pyts@0.12", when="@0.4:0.5")
        depends_on("py-rdt@0.6.1:0.6.1.0,0.6.2:0", when="@0.4:0.5.0")
        depends_on("py-scikit-learn@0.24.0:", when="@0.3.3:0.10")
        depends_on("py-scipy@1.5.4:", when="@0.4:0.8")
        depends_on("py-torch@1.8:1", when="@0.4:0.7")
