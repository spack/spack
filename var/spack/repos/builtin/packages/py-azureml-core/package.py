# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzuremlCore(PythonPackage):
    """The azureml-core contains functionality for creating and managing:
    * Azure Machine Learning workspaces, experiments and runs;
    * Machine learning compute respources;
    * Models, images and web services.
    """

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url = "https://pypi.io/packages/py3/a/azureml_core/azureml_core-1.11.0-py3-none-any.whl"

    version(
        "1.23.0",
        sha256="0965d0741e39cdb95cff5880dbf1a55fdd87cd9fc316884f965668e6cc36e628",
        url="https://pypi.org/packages/b8/4b/203468b7dc8ac633fc65a45c136efed2dca6ee29311db02b2ff1cee260d6/azureml_core-1.23.0-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="df8a01b04bb156852480de0bdd78434ed84f386e1891752bdf887faeaa2ca417",
        url="https://pypi.org/packages/31/6e/851737ab431fca870d5f7927761163875ca5834842b55b0d496a8b93bfb9/azureml_core-1.11.0-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="a0f2b0977f18fb7dcb88c314594a4a85c636a36be3d582be1cae25655fea6105",
        url="https://pypi.org/packages/22/38/6c763c4194b751550fd57fdfebcd3ec1431c0d634f17e004923ea7a4e90c/azureml_core-1.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3.8", when="@:1.34")
        depends_on("py-adal@1.2:", when="@:1.31")
        depends_on("py-azure-common@1.1.12:", when="@:1.26")
        depends_on("py-azure-graphrbac@0.40:")
        depends_on("py-azure-mgmt-authorization@0.40:0", when="@1.16:1.40")
        depends_on("py-azure-mgmt-authorization@0.40:", when="@:1.15")
        depends_on("py-azure-mgmt-containerregistry@2:", when="@:1.37")
        depends_on("py-azure-mgmt-keyvault@0.40:2", when="@1.16:1.29")
        depends_on("py-azure-mgmt-keyvault@0.40:", when="@:1.14")
        depends_on("py-azure-mgmt-network@10", when="@1.5:1.9")
        depends_on("py-azure-mgmt-resource@1.2.1:13", when="@1.16:1.36")
        depends_on(
            "py-azure-mgmt-resource@1.2.1:",
            when="@:1.9.0.0,1.10:1.10.0.post1,1.11:1.11.0.post1,1.12:1.12.0.post1,1.13:1.13.0.0,"
            "1.14:1.14.0.0",
        )
        depends_on("py-azure-mgmt-storage@1.5:11", when="@1.16:1.36")
        depends_on("py-azure-mgmt-storage@1.5:", when="@:1.14")
        depends_on("py-backports-tempfile")
        depends_on("py-contextlib2", when="@:1.26")
        depends_on("py-cryptography@:1.8,2.3:3.2.0", when="@1.23:1.24.0.post1")
        depends_on("py-cryptography@:1.8,2.3:", when="@:1.22,1.52:1.53")
        depends_on("py-docker", when="@:1.26")
        depends_on("py-jmespath", when="@:1.26")
        depends_on("py-jsonpickle", when="@:1.26")
        depends_on("py-msrest@0.5.1:", when="@:1.26")
        depends_on("py-msrestazure@0.4.33:", when="@:1.31")
        depends_on("py-ndg-httpsclient", when="@:1.31")
        depends_on("py-pathspec", when="@:1.26")
        depends_on(
            "py-pyjwt",
            when="@:1.13.0.post1,1.14:1.14.0.post1,1.15:1.15.0.0,1.16:1.16.0.post1,1.17:1.17.0.0,"
            "1.22:",
        )
        depends_on("py-pyopenssl@:20", when="@1.21:1.36")
        depends_on("py-pyopenssl", when="@:1.15")
        depends_on("py-python-dateutil@2.7.3:", when="@:1.26")
        depends_on("py-pytz")
        depends_on("py-requests@2.19.1:", when="@:1.36")
        depends_on(
            "py-ruamel-yaml@0.15.35:", when="@1.11.0.post:1.11,1.12.0.post:1.25.0.0,1.26:1.26.0.0"
        )
        depends_on("py-ruamel-yaml@0.16.9:", when="@1.5.0.post4:1.11.0.0,1.12:1.12.0.0")
        depends_on("py-secretstorage", when="@:1.26")
        depends_on("py-urllib3@1.23:", when="@:1.31")
