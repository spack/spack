# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Proj(AutotoolsPackage):
    """PROJ is a generic coordinate transformation software, that transforms
    geospatial coordinates from one coordinate reference system (CRS) to
    another. This includes cartographic projections as well as geodetic
    transformations."""

    homepage = "https://proj4.org/"
    url      = "http://download.osgeo.org/proj/proj-5.0.1.tar.gz"

    version('5.0.1', '15c8d7d6a8cb945c7878d0ff322a232c')
    version('4.9.2', '9843131676e31bbd903d60ae7dc76cf9')
    version('4.9.1', '3cbb2a964fd19a496f5f4265a717d31c')
    version('4.8.0', 'd815838c92a29179298c126effbb1537')
    version('4.7.0', '927d34623b52e0209ba2bfcca18fe8cd')
    version('4.6.1', '7dbaab8431ad50c25669fd3fb28dc493')

    # https://github.com/OSGeo/proj.4#distribution-files-and-format
    # https://github.com/OSGeo/proj-datumgrid
    resource(
        name='proj-datumgrid',
        url='https://download.osgeo.org/proj/proj-datumgrid-1.7.tar.gz',
        md5='6799bd8ac411b8a78724e34850c206c4',
        placement='nad'
    )

    def configure_args(self):
        return [
            'PROJ_LIB={0}'.format(join_path(self.stage.source_path, 'nad'))
        ]
