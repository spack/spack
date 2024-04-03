# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypinyin(PythonPackage):
    """Chinese Pinyin conversion module/tool."""

    homepage = "https://github.com/mozillazg/python-pinyin"
    pypi = "pypinyin/pypinyin-0.46.0.tar.gz"

    license("MIT")

    version(
        "0.46.0",
        sha256="7251f4fa0b1e43ad91f6121d9a842e8acd72a6a34deea5e87d2a97621eadc11f",
        url="https://pypi.org/packages/29/24/39eceaa25584f704efc22d7beb17a887fc92425f82180be28bf0486b2c83/pypinyin-0.46.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")
