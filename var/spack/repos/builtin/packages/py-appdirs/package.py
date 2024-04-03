# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAppdirs(PythonPackage):
    """A small Python module for determining appropriate platform-specific
    dirs, e.g. a "user data dir"."""

    homepage = "https://github.com/ActiveState/appdirs"
    pypi = "appdirs/appdirs-1.4.3.tar.gz"

    license("MIT")

    version(
        "1.4.4",
        sha256="a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
        url="https://pypi.org/packages/3b/00/2344469e2084fb287c2e0b57b72910309874c3245463acd6cf5e3db69324/appdirs-1.4.4-py2.py3-none-any.whl",
    )
    version(
        "1.4.3",
        sha256="d8b24664561d0d34ddfaec54636d502d7cea6e29c3eaf68f3df6180863e2166e",
        url="https://pypi.org/packages/56/eb/810e700ed1349edde4cbdc1b2a21e28cdf115f9faf263f6bbf8447c1abf3/appdirs-1.4.3-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="85e58578db8f29538f3109c11250c2a5514a2fcdc9890d9b2fe777eb55517736",
        url="https://pypi.org/packages/7b/8b/eebc6e2002a1e0383f1c7108d0111d4d33ea93bf417d7e19e43ec9b87b2b/appdirs-1.4.0-py2.py3-none-any.whl",
    )
