# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtEventgrid(PythonPackage):
    """Microsoft Azure EventGrid Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-eventgrid/azure-mgmt-eventgrid-2.2.0.zip"

    # Release candidate needed for py-azure-cli
    version(
        "3.0.0-rc7",
        sha256="6ac0ff572a79e93ee3c607ca47de152539d74a74a3bc98360e1c2b0def0edb4a",
        url="https://pypi.org/packages/cb/a5/83a9d0e3919755404ebc5c670ae670ea6c6e60725a251da46eb9a4da186a/azure_mgmt_eventgrid-3.0.0rc7-py2.py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="e370cb7402206ba6f5cb611130835ecf6d4ca52c647766afdfae9e928dfea7e0",
        url="https://pypi.org/packages/f9/d4/57cc437d1a3ec82feadc86fbd6485a3cc3c198d8717c171045e6fb98dd6d/azure_mgmt_eventgrid-2.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@2.0.0-rc2:8")
        depends_on("py-msrestazure@0.4.32:", when="@2.0.0-rc2:3")
