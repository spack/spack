# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySshtunnel(PythonPackage):
    """Pure python SSH tunnels."""

    homepage = "https://github.com/pahaz/sshtunnel"
    pypi = "sshtunnel/sshtunnel-0.1.5.tar.gz"

    license("MIT")

    version(
        "0.1.5",
        sha256="5eee2e414c3fd9e9ef5d058bebece272a6aae928849ef7f2d9561b7fffab7aea",
        url="https://pypi.org/packages/38/7d/6f19be1ee49cee9593c5ac3aa1fb38fe30eaf1520114e08dee2ab2a45855/sshtunnel-0.1.5-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-paramiko@1.15.2:", when="@0.1.3:0.1.3.0,0.1.5:0.3")
