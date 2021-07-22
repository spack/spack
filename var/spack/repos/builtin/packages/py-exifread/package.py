# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyExifread(PythonPackage):
    """Read Exif metadata from tiff and jpeg files."""

    homepage = "https://github.com/ianare/exif-py"
    pypi     = "ExifRead/ExifRead-2.3.2.tar.gz"

    version('2.3.2', sha256='a0f74af5040168d3883bbc980efe26d06c89f026dc86ba28eb34107662d51766')

    depends_on('py-setuptools', type='build')
