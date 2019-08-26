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

    variant('grass', default=False, description='Build with GRASS providers and plugin')

    # Ref. for dependencies:
    # http://htmlpreview.github.io/?https://raw.github.com/qgis/QGIS/master/doc/INSTALL.html
    depends_on('qt+dbus')
    depends_on('proj@4.4.0:')
    depends_on('geos@3.4.0:')
    depends_on('sqlite@3.0.0:')
    depends_on('libspatialite@4.2.0:')
    depends_on('libspatialindex')
    depends_on('gdal@2.1.0:')
    depends_on('qwt@5:')
    depends_on('qwtpolar')
    depends_on('expat@1.95:')
    depends_on('qca@2.2.1') # need to pass CMAKE_CXX_STANDARD=11 option
    depends_on('py-pyqt4', when='@2')
    depends_on('py-pyqt5@5.3:', when='@3')
    depends_on('qscintilla')
    depends_on('qjson')
    depends_on('py-requests')
    depends_on('py-psycopg2')
    depends_on('qtkeychain@0.5:', when='@3:')
    depends_on('libzip')
    depends_on('exiv2')
    depends_on('python@3.0.0:', type=('build', 'run'), when='@3')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='@2')

    # optionals
    depends_on('postgresql@8:') # for PostGIS support
    depends_on('gsl') # for georeferencer
    depends_on('grass@7.0.0', type=('build', 'link', 'run'), when='+grass') # for georeferencer

    # build
    depends_on('cmake@3.0.0:', type='build')
    depends_on('flex@2.5.6:', type='build')
    depends_on('bison@2.4:', type='build')

    # Conflicts for newer versions
    conflicts('proj@:4.9.2', when='@3.8.2:')

    # v3.8.1, Qt >= 5.9.0 is required
    conflicts('qt@:5.8.99', when='@3.8.1:')

    # conflicts for qgis@2, qt@4, python@2
    conflicts('qtkeychain@0.6.0:', when='^qt@4')
    conflicts('qt@5:', when='@2')

    def cmake_args(self):
        args = []
        # qtwebkit module was removed from qt as of version 5.6
        # needs to be compiled as a separate package
        args.append('-DWITH_QTWEBKIT=OFF')
        # cmake couldn't determine the following paths
        args.append("-DEXPAT_LIBRARY={0}".format(self.spec['expat'].libs))
        args.append('-DLIBZIP_CONF_INCLUDE_DIR='+str(self.spec['libzip'].libs)+'/pkgconfig')
        args.append('-DPOSTGRES_PREFIX={0}'.format(self.spec['postgresql'].prefix))
        args.append('-DQSCINTILLA_INCLUDE_DIR='+str(self.spec['qscintilla'].prefix)+'/include')
        args.append('-DQSCINTILLA_LIBRARY='+str(self.spec['qscintilla'].prefix)+'/lib')
        return args
