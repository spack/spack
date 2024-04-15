# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsUnixsocket(PythonPackage):
    """Use requests to talk HTTP via a UNIX domain socket."""

    homepage = "https://github.com/msabramo/requests-unixsocket"
    pypi = "requests-unixsocket/requests-unixsocket-0.2.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.0",
        sha256="c685c680f0809e1b2955339b1e5afc3c0022b3066f4f7eb343f43a6065fc0e5d",
        url="https://pypi.org/packages/b3/63/e9e81d5e7370d46f08407c37399b507725125587b01fff46b4da5ddd3a4a/requests_unixsocket-0.3.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="014d07bfb66dc805a011a8b4b306cf4ec96d2eddb589f6b2b5765e626f0dc0cc",
        url="https://pypi.org/packages/d0/63/97662a6f7175c08381447a09f6bc35464075f0ea6549cf6daf2668b51f04/requests_unixsocket-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-requests@1.1:", when="@0.2:")
        depends_on("py-urllib3@1.8:", when="@0.2")
