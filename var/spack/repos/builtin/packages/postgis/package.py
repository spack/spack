# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Postgis(AutotoolsPackage):
    """
    PostGIS is a spatial database extender for PostgreSQL object-relational
    database. It adds support for geographic objects allowing location
    queries to be run in SQL
    """

    homepage = "https://postgis.net/"
    url      = "https://download.osgeo.org/postgis/source/postgis-2.5.3.tar.gz"

    version('3.1.1', sha256='0e96afef586db6939d48fb22fbfbc9d0de5e6bc1722d6d553d63bb41441a2a7d')
    version('3.1.0', sha256='da06e2456876cd0c6a9bee0636ff700982e900c597d1e4cb80a99a2623400201')
    version('3.0.3', sha256='07fedbd046cbed55d24bb22474890a4651d0223b6e12d2dac1517b9a43674817')
    version('3.0.2', sha256='a3a1641dfd73c83924088a185bdb8b35567b3d1dc8d0887f9e4b492e228ab2ca')
    version('3.0.1', sha256='5a5432f95150d9bae9215c6d1c7bb354e060482a7c379daa9b8384e1d03e6353')
    version('3.0.0', sha256='c06fd2cd5cea0119106ffe17a7235d893c2bbe6f4b63c8617c767630973ba594')
    version('2.5.3', sha256='72e8269d40f981e22fb2b78d3ff292338e69a4f5166e481a77b015e1d34e559a')

    variant('gui', default=False, description='Build with GUI support, creating shp2pgsql-gui graphical interface to shp2pgsql')

    # Refs:
    # https://postgis.net/docs/postgis_installation.html
    # https://postgis.net/source/

    depends_on('postgresql')
    depends_on('geos')
    depends_on('proj')
    depends_on('gdal')
    depends_on('libxml2')
    depends_on('json-c')

    depends_on('sfcgal')
    depends_on('pcre')
    depends_on('perl', type=('build', 'run'))
    depends_on('protobuf-c')

    depends_on('gtkplus@:2.24.32', when='+gui')

    def setup_build_environment(self, env):
        env.set('POSTGIS_GDAL_ENABLED_DRIVERS', 'ENABLE_ALL')

    def setup_run_environment(self, env):
        env.set('POSTGIS_GDAL_ENABLED_DRIVERS', 'ENABLE_ALL')

    def configure_args(self):
        args = []
        args.append('--with-sfcgal=' + str(self.spec['sfcgal'].prefix.bin) +
                    '/sfcgal-config')
        if '+gui' in self.spec:
            args.append('--with-gui')
        return args

    # By default package installs under postgresql prefix.
    # Apparently this is a known bug:
    # https://postgis.net/docs/postgis_installation.html
    # The following modifacations that fixed this issue are found in
    # Guix recipe for postgis.
    # https://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/geo.scm#n720

    def build(self, spec, prefix):
        make('bindir=' + prefix.bin, 'libdir=' + prefix.lib,
             'pkglibdir=' + prefix.lib, 'datadir=' + prefix.share,
             'docdir=' + prefix.share.doc)

    def install(self, spec, prefix):
        make('install', 'bindir=' + prefix.bin, 'libdir=' + prefix.lib,
             'pkglibdir=' + prefix.lib, 'datadir=' + prefix.share,
             'docdir=' + prefix.share.doc)

    @run_before('build')
    def fix_raster_bindir(self):
        makefile = FileFilter('raster/loader/Makefile')
        makefile.filter('$(DESTDIR)$(PGSQL_BINDIR)', self.prefix.bin,
                        string=True)
        makefile = FileFilter('raster/scripts/Makefile')
        makefile.filter('$(DESTDIR)$(PGSQL_BINDIR)', self.prefix.bin,
                        string=True)
