# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtHdinsight(PythonPackage):
    """Microsoft Azure HDInsight Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-hdinsight/azure-mgmt-hdinsight-1.5.1.zip"

    version(
        "1.5.1",
        sha256="53134d367ff7e9529ddc9f9cf00cdbece8be55103a24d37607ed8f53391cec9f",
        url="https://pypi.org/packages/ae/c2/fb2076606f1f72ea299b023d5e0dd18672ca99a51767439cc9272b3d9c2f/azure_mgmt_hdinsight-1.5.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:7")
        depends_on("py-msrestazure@0.4.32:", when="@:3")
