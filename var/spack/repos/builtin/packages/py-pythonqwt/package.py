# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonqwt(PythonPackage):
    """Qt plotting widgets for Python"""

    homepage = "https://github.com/PierreRaybaut/PythonQwt"
    pypi = "PythonQwt/PythonQwt-0.5.5.zip"

    license("LGPL-2.1-or-later")

    version(
        "0.5.5",
        sha256="806d109a0f163ee37259516b498f9b2a711682efbb0dd60dff3c31f25007cbef",
        url="https://pypi.org/packages/46/40/caf045d48f29b579f124a0cc33b140fa7e4ef4a58d9e3356b1efc5276d09/PythonQwt-0.5.5-py2.py3-none-any.whl",
    )
