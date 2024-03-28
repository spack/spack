# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWhichcraft(PythonPackage):
    """Cross-platform cross-python shutil.which functionality."""

    homepage = "https://github.com/pydanny/whichcraft"
    url = "https://github.com/pydanny/whichcraft/archive/0.4.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.1",
        sha256="cd0e10b58960ab877d9f273cd28788730936c3cdaceec2dafad97c7cf3067d46",
        url="https://pypi.org/packages/60/8a/5c52e30e11672f7e3aa61f348ddae443d122bcd96bc8b785ac76dbae944b/whichcraft-0.4.1-py2.py3-none-any.whl",
    )
