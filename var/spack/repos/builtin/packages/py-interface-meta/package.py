# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInterfaceMeta(PythonPackage):
    """A convenient way to expose an extensible API with enforced method
    signatures and consistent documentation."""

    homepage = "https://github.com/matthewwardrop/interface_meta"
    pypi = "interface_meta/interface_meta-1.2.4.tar.gz"

    license("MIT")

    version(
        "1.3.0",
        sha256="de35dc5241431886e709e20a14d6597ed07c9f1e8b4bfcffde2190ca5b700ee8",
        url="https://pypi.org/packages/02/3f/a6ec28c88e2d8e54d32598a1e0b5208a4baa72a8e7f6e241beab5731eb9d/interface_meta-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.4",
        sha256="8d11375064d51e73764a02b8225af87b1ed63c20c1df52d3867611a5e70a5fc0",
        url="https://pypi.org/packages/f1/43/4dddcfe75b42cd4cf285b95c5f3b132c7e13af44dcb3b74b03656072f237/interface_meta-1.2.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3", when="@1.3:")
