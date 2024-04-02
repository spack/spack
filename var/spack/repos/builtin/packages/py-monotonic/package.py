# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonotonic(PythonPackage):
    """An implementation of time.monotonic() for Python 2 & < 3.3"""

    pypi = "monotonic/monotonic-1.6.tar.gz"

    license("Apache-2.0")

    version(
        "1.6",
        sha256="68687e19a14f11f26d140dd5c86f3dba4bf5df58003000ed467e0e2a69bca96c",
        url="https://pypi.org/packages/9a/67/7e8406a29b6c45be7af7740456f7f37025f0506ae2e05fb9009a53946860/monotonic-1.6-py2.py3-none-any.whl",
    )
    version(
        "1.2",
        sha256="668088baea217e1e89edecd12c9a913ab4678419ad4eca378dcef1e4059a44f3",
        url="https://pypi.org/packages/3b/dd/4a10abd8298809aa8c0cbc8defaae292812085ccae8aa14a15400a88ac62/monotonic-1.2-py2.py3-none-any.whl",
    )
