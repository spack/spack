# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCompute(PythonPackage):
    """Microsoft Azure Compute Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-compute/azure-mgmt-compute-13.0.0.zip"

    version(
        "13.0.0",
        sha256="0848fe37b4b6e49bed07d3969789072da7c259e8a8d21458251c3912f695e7c2",
        url="https://pypi.org/packages/f3/5d/e42ae8d9f9ee8ba36a800a8eaf16cd14a0ea6cb79d8cccfb203c505cc802/azure_mgmt_compute-13.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@:30.5")
        depends_on("py-msrest@0.5:", when="@:19")
        depends_on("py-msrestazure@0.4.32:", when="@:14")
