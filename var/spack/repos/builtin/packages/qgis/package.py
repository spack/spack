# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qgis(CMakePackage):
    """QGIS is a free and open-source cross-platform desktop geographic
    information system application that supports viewing, editing, and
    analysis of geospatial data.
    """

    homepage = "https://qgis.org"
    url      = "https://qgis.org/downloads/qgis-3.8.1.tar.bz2"

    version('3.8.1', sha256='d65c8e1c7471bba46f5017f261ebbef81dffb5843a24f0e7713a00f70785ea99')

    # Ref. for dependencies:
    # http://htmlpreview.github.io/?https://raw.github.com/qgis/QGIS/master/doc/INSTALL.html
    depends_on('qt@5.9.0:')
    depends_on('proj@4.4.0:')
    depends_on('geos@3.4.0:')
    depends_on('sqlite@3.0.0:')
    depends_on('libspatialite@4.2.0:')
    depends_on('libspatialindex')
    depends_on('gdal@2.1.0:')
    depends_on('qwt')
    depends_on('qwtpolar')
    depends_on('expat')
    depends_on('qca@2.2.1') # need to pass CMAKE_CXX_STANDARD=11 option
    depends_on('py-pyqt5')
    depends_on('qscintilla')
    depends_on('gsl')
    depends_on('qjson')
    depends_on('requests')
    depends_on('py-psycopg2')
    depends_on('python@3.0.0:')
    #depends_on('qtkeychain') # Not implemented yet, is it a "key" dependency?

    depends_on('cmake@3.0.0:', type='build')
    depends_on('flex@2.5.6:', type='build')
    depends_on('bison@2.4:', type='build')

#    def cmake_args(self):
#        # FIXME: Add arguments other than
#        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
#        # FIXME: If not needed delete this function
#        args = []
#        return args
