# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFonttools(PythonPackage):
    """fontTools is a library for manipulating fonts, written in Python.

    The project includes the TTX tool, that can convert TrueType and OpenType fonts to
    and from an XML text format, which is also called TTX. It supports TrueType,
    OpenType, AFM and to an extent Type 1 and some Mac-specific formats."""

    homepage = "https://github.com/fonttools/fonttools"
    pypi = "fonttools/fonttools-4.28.1.zip"

    skip_modules = ["fontTools.ufoLib"]

    license("MIT")

    version(
        "4.37.3",
        sha256="a5bc5f5d48faa4085310b8ebd4c5d33bf27c6636c5f10a7de792510af2745a81",
        url="https://pypi.org/packages/cc/1c/ed3d02ee49952bab33318269bbc316cde6b92205ca77224e558de76f1cd6/fonttools-4.37.3-py3-none-any.whl",
    )
    version(
        "4.31.2",
        sha256="2df636a3f402ef14593c6811dac0609563b8c374bd7850e76919eb51ea205426",
        url="https://pypi.org/packages/b0/5c/5dd502b0e2e0cb2980fc4ed17e970089003e377115abf79b1918097f4996/fonttools-4.31.2-py3-none-any.whl",
    )
    version(
        "4.29.1",
        sha256="1933415e0fbdf068815cb1baaa1f159e17830215f7e8624e5731122761627557",
        url="https://pypi.org/packages/1d/46/65a58d7b92905e2767000b3f6eb1d0301e9ed7d459d14461075c1db63349/fonttools-4.29.1-py3-none-any.whl",
    )
    version(
        "4.28.1",
        sha256="68071406009e7ef6a5fdcd85d95975cd6963867bb226f2b786bfffe15d1959ef",
        url="https://pypi.org/packages/42/98/897d6a04ca4a3927dcd6f1237c5d5c49e068962fd4f2c015463a50ba07ed/fonttools-4.28.1-py3-none-any.whl",
    )
    version(
        "4.26.2",
        sha256="47ce4aedc815a9d101d3b522c580264ca7e4a921cca6183ed460ad2c65d46f98",
        url="https://pypi.org/packages/a4/73/0364d5ce3cb43b3568fc756b86a633ad1f4c7f6d9a380fb39b9f21d6fb93/fonttools-4.26.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.28:4.38.0")
