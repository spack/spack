# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyshp(PythonPackage):
    """The Python Shapefile Library (pyshp) reads and writes ESRI Shapefiles in
    pure Python."""

    homepage = "https://github.com/GeospatialPython/pyshp"
    url      = "https://pypi.io/packages/source/p/pyshp/pyshp-1.2.12.tar.gz"

    version('1.2.12', '63d33d151ac308f1db71ea0f22c30d8b')

    depends_on('py-setuptools', type='build')
