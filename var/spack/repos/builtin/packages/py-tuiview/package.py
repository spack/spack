# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTuiview(PythonPackage):
    """TuiView is a lightweight raster GIS with powerful raster attribute
    table manipulation abilities.
    """

    homepage = "https://bitbucket.org/chchrsc/tuiview"
    url      = "https://bitbucket.org/chchrsc/tuiview/get/tuiview-1.1.7.tar.gz"

    version('1.1.7', '4b3b38a820cc239c8ab4a181ac5d4c30')

    depends_on("py-pyqt4", type=('build', 'run'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on("gdal")
