# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH11(PythonPackage):
    """A pure-Python, bring-your-own-I/O implementation of HTTP/1.1"""

    homepage = "https://github.com/python-hyper/h11"
    pypi = "h11/h11-0.10.0.tar.gz"

    license("MIT")

    version(
        "0.13.0",
        sha256="8ddd78563b633ca55346c8cd41ec0af27d3c79931828beffb46ce70a379e7442",
        url="https://pypi.org/packages/19/d2/32a15a4955be1b8114a1c570999eefd31279c7f9aa2d2a43d492a79b53c5/h11-0.13.0-py3-none-any.whl",
    )
    version(
        "0.12.0",
        sha256="36a3cb8c0a032f56e2da7084577878a035d3b61d104230d4bd49c0c6b555a9c6",
        url="https://pypi.org/packages/60/0f/7a0eeea938eaf61074f29fed9717f2010e8d0e0905d36b38d3275a1e4622/h11-0.12.0-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="ab6c335e1b6ef34b205d5ca3e228c9299cc7218b049819ec84a388c2525e5d87",
        url="https://pypi.org/packages/b2/79/9c5f5cd738ec2a9b26453b3093915c0999f24454e2773921025c03b5509e/h11-0.11.0-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="9eecfbafc980976dbff26a01dd3487644dd5d00f8038584451fc64a660f7c502",
        url="https://pypi.org/packages/1f/0d/9a3a4de68d76bbacd4851ed9be9aeef8f170532d3907e009fe1fda81d350/h11-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="4bc6d6a1238b7615b266ada57e0618568066f57dd6fa967d1290ec9309b2f2f1",
        url="https://pypi.org/packages/5a/fd/3dad730b0f95e78aeeb742f96fa7bbecbdd56a58e405d3da440d5bfb90c6/h11-0.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses", when="@0.13 ^python@:3.6")
        depends_on("py-typing-extensions", when="@0.13: ^python@:3.7")
