# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlDatasetRuntime(PythonPackage):
    """The purpose of this package is to coordinate dependencies within
    AzureML packages. It is not intended for public use."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml-dataset-runtime/azureml_dataset_runtime-1.11.0.post1-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="96ca73d03ffedc0dd336d9383d2e17cf74548a89fc7ca4c201c599817c97bbc6",
        url="https://pypi.org/packages/a5/0f/c38e53baeadba7f5fea738a127116dd666a0893fc8f6b1d27f5bc5f91c6a/azureml_dataset_runtime-1.23.0-py3-none-any.whl",
    )

    variant("fuse", default=False, description="Build with FUSE support")

    with default_args(type="run"):
        depends_on("py-azureml-dataprep@2.10", when="@1.23")
        depends_on("py-fusepy@3:", when="+fuse")
        depends_on("py-numpy@:1.19.2,1.19.4:", when="@1.19.0.post:1.48 platform=linux")
        depends_on("py-numpy@:1.19.3", when="@1.19.0.post:1.31 platform=windows")
        depends_on("py-pyarrow@0.17:1", when="@:1.27")
