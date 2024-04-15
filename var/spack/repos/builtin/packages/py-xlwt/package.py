# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXlwt(PythonPackage):
    """Library to create spreadsheet files compatible with
    MS Excel 97/2000/XP/2003 XLS files, on any platform,
    with Python 2.6, 2.7, 3.3+."""

    pypi = "xlwt/xlwt-1.3.0.tar.gz"

    version(
        "1.3.0",
        sha256="a082260524678ba48a297d922cc385f58278b8aa68741596a87de01a9c628b2e",
        url="https://pypi.org/packages/44/48/def306413b25c3d01753603b1a222a011b8621aed27cd7f89cbc27e6b0f4/xlwt-1.3.0-py2.py3-none-any.whl",
    )
