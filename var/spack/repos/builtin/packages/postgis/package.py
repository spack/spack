# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('3.0.0alpha4', sha256='f20b38fe002a5d5f1a9f8d9ee16a55cb284ad3b4606cacefa0e43e1c2ef2e4dd')
    version('2.5.3', preferred=True, sha256='72e8269d40f981e22fb2b78d3ff292338e69a4f5166e481a77b015e1d34e559a')

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
    depends_on('perl')
    depends_on('protobuf-c')

    depends_on('gtkplus@:2.24.32', when='+gui')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('POSTGIS_GDAL_ENABLED_DRIVERS', 'ENABLE_ALL')

    def configure_args(self):
        args = []
        args.append('--with-sfcgal=' + str(self.spec['sfcgal'].prefix.bin) +
                    '/sfcgal-config')
        if '+gui' in self.spec:
            args.append('--with-gui')
        return args
