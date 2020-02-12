# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyshp(PythonPackage):
    """The Python Shapefile Library (pyshp) reads and writes ESRI Shapefiles in
    pure Python."""

    homepage = "https://github.com/GeospatialPython/pyshp"
    url      = "https://pypi.io/packages/source/p/pyshp/pyshp-1.2.12.tar.gz"

    version('1.2.12', sha256='8dcd65e0aa2aa2951527ddb7339ea6e69023543d8a20a73fc51e2829b9ed6179')

    depends_on('py-setuptools', type='build')
