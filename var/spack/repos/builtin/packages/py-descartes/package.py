# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDescartes(PythonPackage):
    """Use Shapely or GeoJSON-like geometric objects as matplotlib paths
       and patches"""

    homepage = "https://pypi.org/project/descartes/"
    url      = "https://pypi.io/packages/source/d/descartes/descartes-1.1.0.tar.gz"

    version('1.1.0', 'ac608090f3c9f6e0ce856fdc29944096')

    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
