# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImagesize(PythonPackage):
    """Parses image file headers and returns image size. Supports PNG, JPEG,
    JPEG2000, and GIF image file formats."""

    homepage = "https://github.com/shibukawa/imagesize_py"
    pypi = "imagesize/imagesize-0.7.1.tar.gz"

    license("MIT")

    version(
        "1.4.1",
        sha256="0d8d18d08f840c19d0ee7ca1fd82490fdc3729b7ac93f49870406ddde8ef8d8b",
        url="https://pypi.org/packages/ff/62/85c4c919272577931d407be5ba5d71c20f0b616d31a0befe0ae45bb79abd/imagesize-1.4.1-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="1db2f82529e53c3e929e8926a1fa9235aa82d0bd0c580359c67ec31b2fddaa8c",
        url="https://pypi.org/packages/60/d6/5e803b17f4d42e085c365b44fda34deb0d8675a1a910635930b831c43f07/imagesize-1.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="3f349de3eb99145973fefb7dbe38554414e5c30abd0c8e4b970a7c9d09f3a1d8",
        url="https://pypi.org/packages/fc/b6/aef66b4c52a6ad6ac18cf6ebc5731ed06d8c9ae4d3b2d9951f261150be67/imagesize-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="6ebdc9e0ad188f9d1b2cdd9bc59cbe42bf931875e829e7a595e6b3abdc05cdfb",
        url="https://pypi.org/packages/29/e9/342106962eac603ff7865a29de05e965af6a259e30fbccc6fc5aeac74d70/imagesize-0.7.1-py2.py3-none-any.whl",
    )
