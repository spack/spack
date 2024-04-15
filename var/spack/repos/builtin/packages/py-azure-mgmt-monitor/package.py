# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtMonitor(PythonPackage):
    """Microsoft Azure Monitor Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-monitor/azure-mgmt-monitor-0.11.0.zip"

    version(
        "0.11.0",
        sha256="91a8dc65c561abb0d1526a584763128adebc1ba9ccb1fbf7e91ab57e772a40d8",
        url="https://pypi.org/packages/ec/5e/a8904655a08522367ba1e4a08db9c3b998875641281d9f31bfb4041a6048/azure_mgmt_monitor-0.11.0-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="3b2a19d712884f20f2b1af88fbd8a28b063b63613642076e605b5622c58f3466",
        url="https://pypi.org/packages/0c/21/14ade188b3a49aa01d024d002dc190197206d85b1be97e51f978ef318f06/azure_mgmt_monitor-0.10.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@0.5:")
        depends_on("py-msrest@0.5:", when="@0.6:2")
        depends_on("py-msrestazure@0.4.32:", when="@0.6:0")
