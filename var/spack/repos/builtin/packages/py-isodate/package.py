# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsodate(PythonPackage):
    """This module implements ISO 8601 date, time and duration parsing. The
    implementation follows ISO8601:2004 standard, and implements only date/time
    representations mentioned in the standard. If something is not mentioned
    there, then it is treated as non existent, and not as an allowed option."""

    homepage = "https://github.com/gweis/isodate/"
    pypi = "isodate/isodate-0.6.0.tar.gz"

    version(
        "0.6.1",
        sha256="0751eece944162659049d35f4f549ed815792b38793f07cf73381c1c87cbed96",
        url="https://pypi.org/packages/b6/85/7882d311924cbcfc70b1890780763e36ff0b140c7e51c110fc59a532f087/isodate-0.6.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="aa4d33c06640f5352aca96e4b81afd8ab3b47337cc12089822d6f322ac772c81",
        url="https://pypi.org/packages/9b/9f/b36f7774ff5ea8e428fdcfc4bb332c39ee5b9362ddd3d40d9516a55221b2/isodate-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@0.6.1:")
