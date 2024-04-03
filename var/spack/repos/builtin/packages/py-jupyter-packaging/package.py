# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterPackaging(PythonPackage):
    """Jupyter Packaging Utilities."""

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi = "jupyter_packaging/jupyter_packaging-0.10.4.tar.gz"

    tags = ["build-tools"]

    license("BSD-3-Clause")

    version(
        "0.12.0",
        sha256="a90902c8b8718c4e1164dfe275b611fbf67fee6bf0070587a735d601010ae81b",
        url="https://pypi.org/packages/81/c4/35ced77bca9893e7fd7df77559457d2e54639758ab93d66dd221f5880a85/jupyter_packaging-0.12.0-py2.py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="6af8b2b76b7978d1c6b75cf31244d646aaca727fc9d0d61f6c7d1bf1c9f49dcd",
        url="https://pypi.org/packages/16/03/87c90528b5a5098b54f91bff64351ce2ad02e2339b067a3987a1538a9ea8/jupyter_packaging-0.11.1-py2.py3-none-any.whl",
    )
    version(
        "0.10.6",
        sha256="c7ebe7bd6a7705df9b9141cbf6be6cc8f177323bb359b703707955f3acef9390",
        url="https://pypi.org/packages/ba/b1/46e0ff67f3211329426565241d201142f5e92bfdf1e52b0c9aaea3ddf0c9/jupyter_packaging-0.10.6-py2.py3-none-any.whl",
    )
    version(
        "0.10.4",
        sha256="0875c5230e1bd5484b0b36efb53302d7fe2ae7c35735db1c4df9993366c0dc46",
        url="https://pypi.org/packages/7d/50/00526d606d22aeeda453f67d086f86125ae5c57f13952b202616b553c8d6/jupyter_packaging-0.10.4-py2.py3-none-any.whl",
    )
    version(
        "0.7.12",
        sha256="e36efa5edd52b302f0b784ff2a4d1f2cd50f7058af331151315e98b73f947b8d",
        url="https://pypi.org/packages/44/90/1ee67d0ca65bd507872accab7dfaad085ea9f9d74c7379b523dfd0498c0f/jupyter_packaging-0.7.12-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.11:")
        depends_on("py-deprecation", when="@0.8:")
        depends_on("py-packaging", when="@0.7.3:")
        depends_on("py-setuptools@60.2:", when="@0.12:")
        depends_on("py-setuptools@46.4:", when="@0.8,0.9.2:0.11")
        depends_on("py-tomlkit", when="@0.8:")
        depends_on("py-wheel", when="@0.8:")

    # https://github.com/jupyter/jupyter-packaging/issues/130
