# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrandalf(PythonPackage):
    """Grandalf is a Python package made for experimentations with graph
    drawing algorithms."""

    homepage = "https://github.com/bdcht/grandalf"
    url = "https://github.com/bdcht/grandalf/archive/v0.7.tar.gz"

    license("EPL-1.0")

    version(
        "0.7",
        sha256="0ba234b8962420a093af39de82e89b22e9152d54b05d2fa30953ce39fa52aea3",
        url="https://pypi.org/packages/8d/5c/badfda0c15bbae6401f5a48ed2adb6e75902ae796bf5f69385948255e9c1/grandalf-0.7-py3-none-any.whl",
    )
    version(
        "0.6",
        sha256="357946e2fd35fc92c327cf3c091acc5aef93e0c74c60fed0a727d827ab3b1272",
        url="https://pypi.org/packages/54/f4/a0b6a4c6d616d0a838b2dd0bc7bf74d73e8e8cdc880bab7fdb5fdc3d0e06/grandalf-0.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-future", when="@:0.6")
        depends_on("py-pyparsing")
