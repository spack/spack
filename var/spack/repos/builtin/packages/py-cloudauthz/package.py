# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCloudauthz(PythonPackage):
    """Implements means of authorization delegation on cloud-based resource providers."""

    homepage = "https://github.com/galaxyproject/cloudauthz"
    pypi = "cloudauthz/cloudauthz-0.6.0.tar.gz"

    license("MIT")

    version(
        "0.6.0",
        sha256="e76e65c9fa3f3e1c63d44bd4488e0d75c0ede919870e0e9f08eae21f1316193b",
        url="https://pypi.org/packages/61/4f/390c7c2d1b2777e8a4a70c295e911778b41a14f5936dec70ed5646d0c767/cloudauthz-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-adal@1.0.2:", when="@0.1:")
        depends_on("py-requests@2.18.4:", when="@0.1:")
