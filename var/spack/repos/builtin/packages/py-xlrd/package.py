# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXlrd(PythonPackage):
    """Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files"""

    homepage = "http://www.python-excel.org/"
    pypi = "xlrd/xlrd-0.9.4.tar.gz"

    version(
        "2.0.1",
        sha256="6a33ee89877bd9abc1158129f6e94be74e2679636b8a205b43b85206c3f0bbdd",
        url="https://pypi.org/packages/a6/0c/c2a72d51fe56e08a08acc85d13013558a2d793028ae7385448a6ccdfae64/xlrd-2.0.1-py2.py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="3b06b6c24970be82a38aa22f77d8f65bf5286dd801bfb62e6b9d168d08ba91cc",
        url="https://pypi.org/packages/48/d1/2d2850ca86bb2e850dc30387c8d7080ca7b611544ea8724e66fc716527fd/xlrd-0.9.4-py3-none-any.whl",
    )
