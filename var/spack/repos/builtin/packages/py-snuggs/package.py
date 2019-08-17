# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySnuggs(PythonPackage):
    """Snuggs are s-expressions for Numpy"""

    homepage = "https://github.com/mapbox/snuggs"""
    url      = "https://github.com/mapbox/snuggs/archive/1.4.1.zip"

    version('1.4.1', 'bfc4058c32faa4ef76ab7946755557cc')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
