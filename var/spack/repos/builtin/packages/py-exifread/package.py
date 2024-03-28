# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExifread(PythonPackage):
    """Read Exif metadata from tiff and jpeg files."""

    homepage = "https://github.com/ianare/exif-py"
    pypi = "ExifRead/ExifRead-2.3.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.0.0",
        sha256="2c5c59ef03b3bbee75b82b82d2498006b3c13509f35c9a76c7552faff73fa2d5",
        url="https://pypi.org/packages/db/d6/189b0016ae8995ad94cd6e2573baf0c289ff862996821d4e42eb6a0206e3/ExifRead-3.0.0-py3-none-any.whl",
    )
    version(
        "2.3.2",
        sha256="3ef8725efdb66530b4b3cd1c4ba5d3f3b35a7872137d2c707f711971f8ebf809",
        url="https://pypi.org/packages/91/c6/177a40fefa6e9ed1a10f0f98863a7137b0a89c4eae5609b9737926dba85f/ExifRead-2.3.2-py3-none-any.whl",
    )
