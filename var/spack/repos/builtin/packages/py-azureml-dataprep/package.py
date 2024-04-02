# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlDataprep(PythonPackage):
    """Azure ML Data Preparation SDK."""

    homepage = "https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py"
    url = "https://pypi.io/packages/py3/a/azureml_dataprep/azureml_dataprep-2.0.2-py3-none-any.whl"

    version(
        "2.11.0",
        sha256="755c0d7cfe228705aee7adc97813fb6d7d6ecb048b66f47c1fd5897f2709c3a2",
        url="https://pypi.org/packages/b5/2d/93d4f59df163f5ac3569df36f2e59c26ecd234576c782ffe6a5da4664532/azureml_dataprep-2.11.0-py3-none-any.whl",
    )
    version(
        "2.10.1",
        sha256="a36f807112ff1e64d21265b8e7f40154c93e3bead539e2a74c9d74200fd77c86",
        url="https://pypi.org/packages/e8/bb/7067a58daf81e32bae7dd92a38b46d6fe35a1b2bcf69d4e77f7254703032/azureml_dataprep-2.10.1-py3-none-any.whl",
    )

    variant("fuse", default=False, description="Build with FUSE support")

    with default_args(type="run"):
        depends_on("py-azure-identity@1.2:1.4", when="@:2.23")
        depends_on("py-azureml-dataprep-native@30", when="@2.10:2.11")
        depends_on("py-azureml-dataprep-rslex@1.9", when="@2.11")
        depends_on("py-azureml-dataprep-rslex@1.8", when="@2.10")
        depends_on("py-cloudpickle@1.1:1", when="@:2.25")
        depends_on("py-dotnetcore2@2.1.14:2", when="@:3")
        depends_on("py-fusepy@3:", when="+fuse")
