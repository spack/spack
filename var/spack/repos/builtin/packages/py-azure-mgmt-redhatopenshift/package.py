# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRedhatopenshift(PythonPackage):
    """Microsoft Azure Red Hat Openshift Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-redhatopenshift/azure-mgmt-redhatopenshift-0.1.0.zip"

    version(
        "0.1.0",
        sha256="2382617f425472fa605c5a97278f7c24ba4495ce0ce0cec25a23829ad9f2f095",
        url="https://pypi.org/packages/ca/e8/1875695efaca6eaa7bdb4ed77528e655ca9ab3759b42107675d80a677efa/azure_mgmt_redhatopenshift-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
