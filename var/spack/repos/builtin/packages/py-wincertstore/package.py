# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWincertstore(PythonPackage):
    """wincertstore provides an interface to access Windows' CA and CRL certificates.
    It uses ctypes and Windows's sytem cert store API through crypt32.dll."""

    homepage = "https://github.com/tiran/wincertstore"
    pypi = "wincertstore/wincertstore-0.2.zip"

    license("PSF-2.0")

    version(
        "0.2",
        sha256="22d5eebb52df88a8d4014d5cf6d1b6c3a5d469e6c3b2e2854f3a003e48872356",
        url="https://pypi.org/packages/d1/67/12f477fa1cc8cbcdc78027c9fb0933ad41daf2e95a29d1cc8f34fe80c692/wincertstore-0.2-py2.py3-none-any.whl",
    )
