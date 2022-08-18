# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPetastorm(PythonPackage):
    """Petastorm is a library enabling the use of Parquet storage from
    Tensorflow, Pytorch, and other Python-based ML training frameworks."""

    homepage = "https://github.com/uber/petastorm"
    url = "https://github.com/uber/petastorm/archive/refs/tags/v0.11.4.tar.gz"

    maintainers = ["adamjstewart"]

    version("0.11.4", sha256="7090dfc86f110e641d95798bcc75f8b1ca14cd56ed3feef491baaa6849629e51")
    version("0.9.8", sha256="571855224411b88b759ba5d48b288ad2ba09997ebd259292f72b9246144b8101")
    version("0.8.2", sha256="1bf4f26ce0b14f7334c0c29868154f1e600021a044f7565a5ad766b5ecdde911")

    depends_on("python@3:", when="@0.9.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-dill@0.2.1:", type=("build", "run"))
    depends_on("py-diskcache@3.0.0:", type=("build", "run"))
    depends_on("py-future@0.10.2:", type=("build", "run"))
    depends_on("py-futures@2.0:", type=("build", "run"), when="^python@:2")
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-packaging@15.0:", type=("build", "run"))
    depends_on("py-pandas@0.19.0:", type=("build", "run"))
    depends_on("py-psutil@4.0.0:", type=("build", "run"))
    depends_on("py-pyspark@2.1.0:", type=("build", "run"))
    depends_on("py-pyzmq@14.0.0:", type=("build", "run"))
    depends_on("py-pyarrow@0.12.0:", type=("build", "run"), when="@:0.8.2")
    depends_on("py-pyarrow@0.17.1:", type=("build", "run"), when="@0.9.8:")
    depends_on("py-six@1.5.0:", type=("build", "run"))
    depends_on("py-fsspec", type=("build", "run"), when="@0.11.4:")
