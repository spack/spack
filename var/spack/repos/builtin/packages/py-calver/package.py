# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCalver(PythonPackage):
    """The calver package is a setuptools extension for automatically
    defining your Python package version as a calendar version."""

    homepage = "https://github.com/di/calver"
    pypi = "calver/calver-2022.6.26.tar.gz"

    license("Apache-2.0")

    version(
        "2022.6.26",
        sha256="a1d7fcdd67797afc52ee36ffb8c8adf6643173864306547bfd1380cbce6310a0",
        url="https://pypi.org/packages/f7/39/e421c06f42ca00fa9cf8929c2466e58a837e8e97b8ab3ff4f4ff9a15e33e/calver-2022.6.26-py3-none-any.whl",
    )
