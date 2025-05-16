# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetatensorLearn(PythonPackage):
    """Building blocks for the atomistic machine learning models based on PyTorch and NumPy"""

    homepage = "https://docs.metatensor.org"
    pypi = "metatensor-learn/metatensor_learn-0.3.2.tar.gz"

    import_modules = ["metatensor.learn"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.3.2", sha256="987f63228888882a6189137ddb89f913b2fde1072c3caa83a39b9f5d50388b51")
    version("0.3.1", sha256="576bf02a83bc513a6a7fea29c864f202d2933386f23a722525bb981d6a55a65c")
    version("0.3.0", sha256="01dd854c40bbc1149cb92aba9c69510f0fcedb7a9d6f4175bb43b1f00838a664")
    version("0.2.3", sha256="c561bc97ab7c5699645140d7494c93d66f7029e02c3c9cd34744ca14f7ef150f")
    version("0.2.2", sha256="ab1b76b2c2a1686a04e811f6d261eb6e7d30c6727ed795c3f55deb61ded98494")

    extends("python@3.9:")

    variant("torch", default=False, description="With PyTorch")

    # pyproject.toml
    depends_on("py-setuptools@68:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("py-pip@22.1:", type="build")
    depends_on("py-torch@2.6:", type="run", when="+torch")
    depends_on("py-numpy", type="run", when="+torch")
    # >=0.3.0 and <0.4.0
    depends_on("py-metatensor-operations@0.3:",
               type="run",
               when="@0.3:")
    conflicts("py-metatensor-operations@0.4.0:",
               when="@0.3:")
