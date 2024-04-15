# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTelemetry(PythonPackage):
    """Machine learning (ML) telemetry package is used to collect telemetry
    data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_telemetry/azureml_telemetry-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="68f9aac77e468db80e60f75d0843536082e2884ab251b6d3054dd623bd9c9e0d",
        url="https://pypi.org/packages/92/1a/85250e6c00b9f09962ee54cc16b7d98a6b8b9125a273c4cbac4cdec54c83/azureml_telemetry-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="0d46c4a7bb8c0b188f1503504a6029384bc2237d82a131e7d1e9e89c3491b1fc",
        url="https://pypi.org/packages/c4/8d/75a63b775a321a23c1b9879335573e16f8b5280b46f721d2881018d72eb0/azureml_telemetry-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="de657efe9773bea0de76c432cbab34501ac28606fe1b380d6883562ebda3d804",
        url="https://pypi.org/packages/d0/72/23a197fc872cbd827c4e0d02f6e6d0de990c677a00472551670aaab5cf6b/azureml_telemetry-1.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@1.2:1.47")
        depends_on("py-applicationinsights")
        depends_on("py-azureml-core@1.23", when="@1.23")
        depends_on("py-azureml-core@1.11", when="@1.11")
        depends_on("py-azureml-core@1.8", when="@1.8")
