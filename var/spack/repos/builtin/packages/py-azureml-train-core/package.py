# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrainCore(PythonPackage):
    """The azureml-train-core contains functionality used by azureml-train
    metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train_core/azureml_train_core-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="5c384ea0bea3ecd8bf2a1832dda906fd183cf2a03ad3372cb824ce8fa417979e",
        url="https://pypi.org/packages/76/69/b8797477bea392fcfea0b1f82634b7bf72fd9e5d9f6c017fabd07f6b1531/azureml_train_core-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="1b5fd813d21e75cd522d3a078eba779333980a309bcff6fc72b74ddc8e7a26f1",
        url="https://pypi.org/packages/5b/37/b6d77bd0b8ddfae0b99b94cf8fa7dafbde3c348bdbaf002ae5e8d4c42ae0/azureml_train_core-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="5a8d90a08d4477527049d793feb40d07dc32fafc0e4e57b4f0729d3c50b408a2",
        url="https://pypi.org/packages/aa/6f/7e4adedc265bb3979c9d3a8ab51ba6d90fa7c4ce6f3f92f3cdda8eae46b9/azureml_train_core-1.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@1.2:1.47")
        depends_on("py-azureml-core@1.23", when="@1.23")
        depends_on("py-azureml-core@1.11", when="@1.11")
        depends_on("py-azureml-core@1.8", when="@1.8")
        depends_on("py-azureml-telemetry@1.23", when="@1.23")
        depends_on("py-azureml-telemetry@1.11", when="@1.11")
        depends_on("py-azureml-telemetry@1.8", when="@1.8")
        depends_on("py-azureml-train-restclients-hyperdrive@1.23", when="@1.23")
        depends_on("py-azureml-train-restclients-hyperdrive@1.11", when="@1.11")
        depends_on("py-azureml-train-restclients-hyperdrive@1.8", when="@1.8")
        depends_on("py-flake8@3.1:3.7", when="@:1.9")
