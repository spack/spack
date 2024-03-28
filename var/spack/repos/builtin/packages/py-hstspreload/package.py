# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHstspreload(PythonPackage):
    """Chromium HSTS Preload list as a Python package and updated daily"""

    homepage = "https://github.com/sethmlarson/hstspreload"
    pypi = "hstspreload/hstspreload-2020.9.23.tar.gz"

    license("BSD-3-Clause")

    version(
        "2020.9.23",
        sha256="d0b5ee3f9f2aa7d2f0c5e8fe7b3b6605eef26a302ba373e0d5a76e7d8e871504",
        url="https://pypi.org/packages/ae/c7/48e6c0c9391b277e47de6040732ffd78a4e518fcea07c7adda37219505c9/hstspreload-2020.9.23-py3-none-any.whl",
    )
