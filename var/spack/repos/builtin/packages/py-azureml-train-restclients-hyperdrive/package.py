# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlTrainRestclientsHyperdrive(PythonPackage):
    """The azureml-train-restclients-hyperdrive contains functionality for
    azureml-train metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_train_restclients_hyperdrive/azureml_train_restclients_hyperdrive-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="8ecee0cdb92a4a431b778ebcc7f9fe7c5bf63ea4cae9caa687980bc34ae3a42c",
        url="https://pypi.org/packages/da/2c/327791786b24c555aa186b624805ba7fd4247ad016af30c2bfb8e5c3e4a5/azureml_train_restclients_hyperdrive-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="8bc6f9676a9f75e6ee06d201c418ea904c24e854f26cf799b08c259c3ac92d13",
        url="https://pypi.org/packages/01/36/c84ad23bf1dba6667ccd912ea86e4da096116bb71a436fc1256061614b5f/azureml_train_restclients_hyperdrive-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="1633c7eb0fd96714f54f72072ccf1c5ee1ef0a8ba52680793f20d27e0fd43c87",
        url="https://pypi.org/packages/da/7f/2fd6bd00e2db910c89181fcac3965377147e29763c397e08cacc5a2c9e95/azureml_train_restclients_hyperdrive-1.8.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@1.2:1.47")
        depends_on("py-msrest@0.5.1:")
        depends_on("py-msrestazure@0.4.33:")
        depends_on("py-requests@2.19.1:")
