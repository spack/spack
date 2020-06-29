# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://download.osgeo.org/proj/proj-6.2.0.tar.gz"

    maintainers = ['adamjstewart']

    # Version 6 removes projects.h, while version 7 removes proj_api.h.
    # Many packages that depend on proj do not yet support the newer API.
    # See https://github.com/OSGeo/PROJ/wiki/proj.h-adoption-status
    version('6.3.1', sha256='6de0112778438dcae30fcc6942dee472ce31399b9e5a2b67e8642529868c86f8')
    version('6.2.0', sha256='b300c0f872f632ad7f8eb60725edbf14f0f8f52db740a3ab23e7b94f1cd22a50')
    version('6.1.0', sha256='676165c54319d2f03da4349cbd7344eb430b225fe867a90191d848dc64788008')
    version('6.0.0', sha256='4510a2c1c8f9056374708a867c51b1192e8d6f9a5198dd320bf6a168e44a3657')
    version('5.2.0', sha256='ef919499ffbc62a4aae2659a55e2b25ff09cccbbe230656ba71c6224056c7e60')
    version('5.1.0', sha256='6b1379a53317d9b5b8c723c1dc7bf2e3a8eb22ceb46b8807a1ce48ef65685bb3')
    version('5.0.1', sha256='a792f78897482ed2c4e2af4e8a1a02e294c64e32b591a635c5294cb9d49fdc8c')
    version('4.9.2', sha256='60bf9ad1ed1c18158e652dfff97865ba6fb2b67f1511bc8dceae4b3c7e657796')
    version('4.9.1', sha256='fca0388f3f8bc5a1a803d2f6ff30017532367992b30cf144f2d39be88f36c319')
    version('4.8.0', sha256='2db2dbf0fece8d9880679154e0d6d1ce7c694dd8e08b4d091028093d87a9d1b5')
    version('4.7.0', sha256='fc5440002a496532bfaf423c28bdfaf9e26cc96c84ccefcdefde911efbd98986')
    version('4.6.1', sha256='76d174edd4fdb4c49c1c0ed8308a469216c01e7177a4510b1b303ef3c5f97b47')

    # https://github.com/OSGeo/proj.4#distribution-files-and-format
    # https://github.com/OSGeo/proj-datumgrid
    resource(
        name='proj-datumgrid',
        url='https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz',
        sha256='3ff6618a0acc9f0b9b4f6a62e7ff0f7bf538fb4f74de47ad04da1317408fcc15',
        placement='nad'
    )

    # @6 appears to be the first version with dependencies
    depends_on('pkgconfig@0.9.0:', type='build', when='@6:')
    depends_on('sqlite@3.7:', when='@6:')

    def configure_args(self):
        return [
            'PROJ_LIB={0}'.format(join_path(self.stage.source_path, 'nad'))
        ]
