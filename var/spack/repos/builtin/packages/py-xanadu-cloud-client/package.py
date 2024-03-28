# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXanaduCloudClient(PythonPackage):
    """The Xanadu Cloud Client (XCC) is a Python API and CLI for the Xanadu Cloud."""

    homepage = "https://github.com/XanaduAI/xanadu-cloud-client"
    pypi = "xanadu-cloud-client/xanadu-cloud-client-0.3.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.0",
        sha256="f96a7a4ef6b0bfe08f21a83c572524fda561f9fbec2b805639f6aa452909d230",
        url="https://pypi.org/packages/51/d7/3c8505a9583ac42d29946f1d46a2fc52c8a4bc2dbd0ebd05a121295c7b1b/xanadu_cloud_client-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-appdirs")
        depends_on("py-fire")
        depends_on("py-numpy")
        depends_on("py-pydantic+dotenv", when="@:0.3.0")
        depends_on("py-python-dateutil")
        depends_on("py-requests")
