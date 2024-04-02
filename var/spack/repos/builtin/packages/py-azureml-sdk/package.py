# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlSdk(PythonPackage):
    """Microsoft Azure Machine Learning Python SDK."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_sdk/azureml_sdk-1.11.0-py3-none-any.whl"

    maintainers("adamjstewart")

    version(
        "1.23.0",
        sha256="b9520f426831acb99fafa1ecd154b6bfd4f73fbf71e918d819f9db4a75438ab9",
        url="https://pypi.org/packages/e0/df/1ac487437507e59216c904aa9d1dbdbcaddd724e3248cb708987de9c482a/azureml_sdk-1.23.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:1.25")
        depends_on("py-azureml-core@1.23", when="@1.23")
        depends_on("py-azureml-dataset-runtime@1.23+fuse", when="@1.23")
        depends_on("py-azureml-pipeline@1.23", when="@1.23")
        depends_on("py-azureml-train@1.23", when="@1.23")
        depends_on("py-azureml-train-automl-client@1.23", when="@1.23")

    # https://github.com/Azure/MachineLearningNotebooks/issues/1285
