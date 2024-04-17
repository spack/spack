# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrain(PythonPackage):
    """The azureml-train package provides estimators for training models using
    different deep learning frameworks and functionality for hyperparameter
    tuning using Azure cloud."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train/azureml_train-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="e16cb8673d9c9c70966c37c7362ceed3514e9797b0816c0aa449730da3b9c857",
        url="https://pypi.org/packages/57/bc/5c2b66e2aca853083827176ddf936a1807aa956ea6a50c88772adc73dc10/azureml_train-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="7800a3067979972b976c81082dc509e23c04405129cc1fdef0f9cd7895bcafc7",
        url="https://pypi.org/packages/2b/73/2a8913ea853e02ec41ad5f1cff6cea32e2a7657cd0035de941847d9eeacd/azureml_train-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="124e5b7d8d64bac61db022f305bd31c25e57fdcb4be93eefd4244a04a13deab3",
        url="https://pypi.org/packages/bc/58/a0ec61bb041f7ff846bea5a7a04a049afe5f8c08604bc9664178178c6077/azureml_train-1.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@1.2:1.47")
        depends_on("py-azureml-train-core@1.23", when="@1.23")
        depends_on("py-azureml-train-core@1.11", when="@1.11")
        depends_on("py-azureml-train-core@1.8", when="@1.8")
