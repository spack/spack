# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCligj(PythonPackage):
    """Click-based argument and option decorators for Python GIS command
    line programs"""

    homepage = "https://github.com/mapbox/cligj"
    url      = "https://github.com/mapbox/cligj/archive/0.5.0.zip"

    version('0.5.0', sha256='ad158722a3f512f7eb33526479acf5cb53d9e59ca15cd494556440839783f106')
    version('0.4.0', 'fe5376068b84c5ed01e2d3adf553e226')

    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
