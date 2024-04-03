# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnidecode(PythonPackage):
    """ASCII transliterations of Unicode text"""

    pypi = "unidecode/Unidecode-1.1.1.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.1.1",
        sha256="1d7a042116536098d05d599ef2b8616759f02985c85b4fef50c78a5aaf10822a",
        url="https://pypi.org/packages/d0/42/d9edfed04228bacea2d824904cae367ee9efd05e6cce7ceaaedd0b0ad964/Unidecode-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "0.4.21",
        sha256="61f807220eda0203a774a09f84b4304a3f93b5944110cc132af29ddb81366883",
        url="https://pypi.org/packages/01/a1/9d7f3138ee3d79a1ab865a2cb38200ca778d85121db19fe264c76c981184/Unidecode-0.04.21-py2.py3-none-any.whl",
    )
