# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Proj(AutotoolsPackage):
    """PROJ is a generic coordinate transformation software, that transforms
    geospatial coordinates from one coordinate reference system (CRS) to
    another. This includes cartographic projections as well as geodetic
    transformations."""

    homepage = "https://proj.org/"
    url      = "http://download.osgeo.org/proj/proj-6.1.0.tar.gz"

    maintainers = ['adamjstewart']

    # Version 6 removes projects.h, while version 7 removes proj_api.h.
    # Many packages that depend on proj do not yet support the newer API.
    # See https://github.com/OSGeo/PROJ/wiki/proj.h-adoption-status
    version('6.1.0', sha256='676165c54319d2f03da4349cbd7344eb430b225fe867a90191d848dc64788008')
    version('6.0.0', sha256='4510a2c1c8f9056374708a867c51b1192e8d6f9a5198dd320bf6a168e44a3657')
    version('5.2.0', 'ad285c7d03cbb138d9246e10e1f3191c')
    version('5.1.0', '68c46f6da7e4cd5708f83fe47af80db6')
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
        url='https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz',
        md5='be7e8f77c12714a4cd53732c1f3cf8d9',
        placement='nad'
    )

    # @6 appears to be the first version with dependencies
    depends_on('pkgconfig@0.9.0:', type='build', when='@6:')
    depends_on('sqlite@3.7:', when='@6:')

    def configure_args(self):
        return [
            'PROJ_LIB={0}'.format(join_path(self.stage.source_path, 'nad'))
        ]
