# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCore(PythonPackage):
    """Microsoft Azure Management Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-mgmt-core"
    pypi = "azure-mgmt-core/azure-mgmt-core-1.2.0.zip"

    license("MIT")

    version(
        "1.4.0",
        sha256="81071675f186a585555ef01816f2774d49c1c9024cb76e5720c3c0f6b337bb7d",
        url="https://pypi.org/packages/b1/5a/3a31578b840600dffb75f3ffb383cc4c5e8ea0d06a1085f86b17e18c3193/azure_mgmt_core-1.4.0-py3-none-any.whl",
    )
    version(
        "1.3.2",
        sha256="fd829f67086e5cf6f7eb016c9e80bb0fb293cbbbd4d8738dc90af9aa1055fb7b",
        url="https://pypi.org/packages/29/99/d06021eb45ff660cd4cf1bf16a60645a8256672edf46ff1976a709a50918/azure_mgmt_core-1.3.2-py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="d36bd595dff6a1509ed52a89ee8dd88b83200320a6afa60fb4186afcb8978ce5",
        url="https://pypi.org/packages/63/a0/2074af80e53b9d50ce9ac3d358778d3eca4508823afec83ea76ba989234b/azure_mgmt_core-1.2.2-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="6966226111e92dff26d984aa1c76f227ce0e8b2069c45c72cfb67f160c452444",
        url="https://pypi.org/packages/4f/da/545b3d2496ac08fb4b4c2d784c8d92cb9bfc843801a53dc870bfafe81f0d/azure_mgmt_core-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="b481a7d4239b11476a2f54e947ccb8c8fdf26dd35f72e13b904e9f1208a0bad6",
        url="https://pypi.org/packages/62/4e/e8b0fbfe9595eb971a6a4438d280b8c67a403421db32e8d1d40215688cf4/azure_mgmt_core-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.4:")
        depends_on("py-azure-core@1.26.2:", when="@1.4:")
        depends_on("py-azure-core@1.24:", when="@1.3.2:1.3")
        depends_on("py-azure-core@1.9:", when="@1.2.2:1.2")
        depends_on("py-azure-core@1.7:", when="@1.2:1.2.0")
        depends_on("py-azure-core@1.4:", when="@1.0.0:1.1")
