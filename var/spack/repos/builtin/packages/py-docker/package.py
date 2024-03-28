# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDocker(PythonPackage):
    """A Python library for the Docker Engine API."""

    homepage = "https://github.com/docker/docker-py"
    pypi = "docker/docker-4.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "6.0.1",
        sha256="dbcb3bd2fa80dca0788ed908218bf43972772009b881ed1e20dfc29a65e49782",
        url="https://pypi.org/packages/d5/b3/a5e41798a6d4b92880998e0d9e6980e57c5d039f7f7144f87627a6b19084/docker-6.0.1-py3-none-any.whl",
    )
    version(
        "5.0.3",
        sha256="7a79bb439e3df59d0a72621775d600bc8bc8b422d285824cb37103eab91d1ce0",
        url="https://pypi.org/packages/54/f3/7af47ead249fbb798d64a0438bad5c26f17ef6ac5cd324d802038eb10d90/docker-5.0.3-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="672f51aead26d90d1cfce84a87e6f71fca401bbc2a6287be18603583620a28ba",
        url="https://pypi.org/packages/2b/80/4eab8a38ff62c31716d07753980a7c5e6550b61096926384f01e742b4a4b/docker-4.2.1-py2.py3-none-any.whl",
    )

    variant("ssh", default=False)

    with default_args(type="run"):
        depends_on("py-packaging", when="@6:")
        depends_on("py-paramiko@2.4.3:", when="@6:+ssh")
        depends_on("py-paramiko@2.4.2:", when="@3.6:5+ssh")
        depends_on("py-pypiwin32@223:", when="@3.5:4.2 platform=windows")
        depends_on("py-pywin32@304:", when="@6: platform=windows")
        depends_on("py-pywin32@227", when="@4.3:5 platform=windows")
        depends_on("py-requests@2.26:", when="@6:")
        depends_on("py-requests@2.14.2:2.17,2.18.1:", when="@3.3,3.4.1:5")
        depends_on("py-six@1.4:", when="@3.3,3.4.1:4")
        depends_on("py-urllib3@1.26:", when="@6:")
        depends_on("py-websocket-client@0.32:", when="@3.3,3.4.1:6")
