# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepsig(PythonPackage):
    """deep-significance: Easy and Better Significance Testing for Deep Neural
    Networks"""

    homepage = "https://github.com/Kaleidophon/deep-significance"
    pypi = "deepsig/deepsig-1.2.1.tar.gz"

    version(
        "1.2.1",
        sha256="f0d2c20d0521c87dea5bb36c25ba755d8502121309c2c8d6efdb240cea978bc8",
        url="https://pypi.org/packages/bb/66/0c530dc27ea0c6063b654ad0ed05a852f34e71ff59c9af5dc54891cb8d71/deepsig-1.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dill@0.3.4", when="@1.1:1.2.5")
        depends_on("py-joblib@1.0.1:1.0", when="@1.0.1:1.2.5")
        depends_on("py-numpy@1.19.5:1.19", when="@1.0.1:1.2.5")
        depends_on("py-pandas@1.3.3", when="@1.1:1.2.5")
        depends_on("py-scipy@1.6.0", when="@1.2:1.2.5")
        depends_on("py-tqdm@4.59", when="@1.0.1:1.2.5")
