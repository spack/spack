# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorlog(PythonPackage):
    """A colored formatter for the python logging module"""

    homepage = "https://github.com/borntyping/python-colorlog"
    pypi = "colorlog/colorlog-4.0.2.tar.gz"

    version(
        "4.0.2",
        sha256="450f52ea2a2b6ebb308f034ea9a9b15cea51e65650593dca1da3eb792e4e4981",
        url="https://pypi.org/packages/68/4d/892728b0c14547224f0ac40884e722a3d00cb54e7a146aea0b3186806c9e/colorlog-4.0.2-py2.py3-none-any.whl",
    )
    version(
        "3.1.4",
        sha256="8b234ebae1ba1237bc79c0d5f1f47b31a3f3e90c0b4c2b0ebdde63a174d3b97b",
        url="https://pypi.org/packages/69/eb/58ae10d3c46a0195ffdd0e3943d255d0d5029d71e5457785ecd665bcf0f3/colorlog-3.1.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama", when="@3.1.4: platform=windows")
