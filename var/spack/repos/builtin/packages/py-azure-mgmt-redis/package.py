# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRedis(PythonPackage):
    """Microsoft Azure Redis Cache Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-redis/azure-mgmt-redis-6.0.0.zip"

    # Release candidate needed for py-azure-cli
    version(
        "7.0.0-rc1",
        sha256="c3e8b24b0f537eb987718dd35eacd4c45f5252d2f5a03dbd011c4c8d074c61ff",
        url="https://pypi.org/packages/d0/94/5a266013edfb3010cdf8fa15e8dc64b966e15cfa9873ee043811ab75eda0/azure_mgmt_redis-7.0.0rc1-py2.py3-none-any.whl",
    )
    version(
        "6.0.0",
        sha256="756fd080868fd057fdaa4b7663985d8ffebd941ad06a4d9786fe4470e65a2114",
        url="https://pypi.org/packages/a1/7e/e958de2ef701104a35caabe4ad5d1588cd2d413271695924c586549d6a34/azure_mgmt_redis-6.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@5:")
        depends_on("py-msrest@0.5:", when="@6:12")
        depends_on("py-msrestazure@0.4.32:", when="@6:7")
