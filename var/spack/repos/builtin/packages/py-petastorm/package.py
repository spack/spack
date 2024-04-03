# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPetastorm(PythonPackage):
    """Petastorm is a library enabling the use of Parquet storage from
    Tensorflow, Pytorch, and other Python-based ML training frameworks."""

    homepage = "https://github.com/uber/petastorm"
    url = "https://github.com/uber/petastorm/archive/refs/tags/v0.11.4.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "0.12.0",
        sha256="02301026559ed2ebed6d662f27629c1f4a3c919a6d10048a0eb37cc8a8b562f5",
        url="https://pypi.org/packages/62/18/ae4a516e536384a2d091953e3fc9df6c61762976e4d3131fe96cbbd88804/petastorm-0.12.0-py2.py3-none-any.whl",
    )
    version(
        "0.11.4",
        sha256="c507ccc321233420905976a7d43ecd46c00beced43e831301b30591b927a520f",
        url="https://pypi.org/packages/0f/fc/cf5dd326cf618c0be91d172f37275f702a7467e6713825da9e591f5d4146/petastorm-0.11.4-py2.py3-none-any.whl",
    )
    version(
        "0.9.8",
        sha256="34cab9a7d028fc3484f1ae80dee1a55291666532175a2dbcbfe5040f1cf5e7d6",
        url="https://pypi.org/packages/67/2c/22c332dee5679e4de091ff613a90eb599f4924e51d766d538aa165aa1893/petastorm-0.9.8-py2.py3-none-any.whl",
    )
    version(
        "0.8.2",
        sha256="e41fcc9b00cf9a92d30dfe213be4e8bab85c33a7a3720b0ea71315e778faa653",
        url="https://pypi.org/packages/f2/de/1cfe0548fb8ef384f40b5c823bed3e7f544f0cccf7cc5cce73cec89373bc/petastorm-0.8.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dill@0.2.1:")
        depends_on("py-diskcache@3:")
        depends_on("py-fsspec", when="@0.10:")
        depends_on("py-future@0.10.2:")
        depends_on("py-numpy@1.13.3:")
        depends_on("py-packaging@15:", when="@0.7.7-rc8:")
        depends_on("py-pandas@0.19.0:")
        depends_on("py-psutil@4:")
        depends_on("py-pyarrow@0.17.1:", when="@0.9.7-rc0:")
        depends_on("py-pyarrow@0.12:", when="@0.8.2:0.9.6")
        depends_on("py-pyspark")
        depends_on("py-pyzmq@14:")
        depends_on("py-six@1.5:")
