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

    maintainers = ['adamjstewart']

    version('3.8.1', sha256='d65c8e1c7471bba46f5017f261ebbef81dffb5843a24f0e7713a00f70785ea99')

    # Ref. for dependencies:
    # http://htmlpreview.github.io/?https://raw.github.com/qgis/QGIS/master/doc/INSTALL.html
    depends_on('qt@5.9.0:+dbus')
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
    depends_on('py-requests')
    depends_on('py-psycopg2')
    depends_on('python@3.0.0:')
    #depends_on('qtkeychain') # Not implemented yet, is it a "key" dependency?

    # more deps discovered during compilation
    depends_on('libzip')
    depends_on('expat')
    depends_on('postgresql')
    depends_on('exiv2')

    depends_on('cmake@3.0.0:', type='build')
    depends_on('flex@2.5.6:', type='build')
    depends_on('bison@2.4:', type='build')

    def cmake_args(self):
        args = []
        args.append("-DEXPAT_LIBRARY={0}".format(self.spec['expat'].libs))
        args.append('-DLIBZIP_CONF_INCLUDE_DIR='+str(self.spec['libzip'].libs)+'/pkgconfig')
        args.append('-DPOSTGRES_PREFIX={0}'.format(self.spec['postgresql'].prefix))
        args.append('-DWITH_QTWEBKIT=OFF')
        args.append('-DQSCINTILLA_INCLUDE_DIR='+str(self.spec['qscintilla'].prefix) + str(self.spec['qt'].prefix)+'/include')
        args.append('-DQSCINTILLA_LIBRARY='+str(self.spec['qscintilla'].prefix) + str(self.spec['qt'].prefix)+'/lib')
        return args
