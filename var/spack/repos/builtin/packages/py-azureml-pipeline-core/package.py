# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlPipelineCore(PythonPackage):
    """Core functionality to enable azureml-pipeline feature."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_pipeline_core/azureml_pipeline_core-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="347e3e41559879611d53eeff5c05dd133db6fa537edcf2b9f70d91aad461df02",
        url="https://pypi.org/packages/db/57/e32064e7b57e59257281888258540d6d76a6021fbfa83b2288bec527d436/azureml_pipeline_core-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="98012195e3bba12bf42ac69179549038b3563b39e3dadab4f1d06407a00ad8b3",
        url="https://pypi.org/packages/d4/e5/49c66f255352c09509354933b753b1281c08eb0b527dd300302d3c83d6e9/azureml_pipeline_core-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="24e1c57a57e75f9d74ea6f45fa4e93c1ee3114c8ed9029d538f9cc8e4f8945b2",
        url="https://pypi.org/packages/a9/04/336adc8a159fadd2586ed74974c41aa22bbdb96bf773c80dac20c71b5bad/azureml_pipeline_core-1.8.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@1.2:1.47")
        depends_on("py-azureml-core@1.23", when="@1.23")
        depends_on("py-azureml-core@1.11", when="@1.11")
        depends_on("py-azureml-core@1.8", when="@1.8")
