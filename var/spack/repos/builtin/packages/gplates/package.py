##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Gplates(CMakePackage):
    """GPlates is desktop software for the interactive visualisation of
    plate-tectonics. GPlates offers a novel combination of interactive
    plate-tectonic reconstructions, geographic information system (GIS)
    functionality and raster data visualisation. GPlates enables both the
    visualisation and the manipulation of plate-tectonic reconstructions
    and associated data through geological time."""

    homepage = 'https://www.gplates.org'
    url      = 'https://sourceforge.net/projects/gplates/files/gplates/2.0/gplates-2.0.0-unixsrc.tar.bz2/download'

    version('2.0.0', '9e95874b35a01f4c9bff5845a1621ad5')

    depends_on('cmake@2.6.2:', type='build')
    # Qt 5 does not support (at least) the Q_WS_* constants.
    depends_on('qt+opengl@4.4.0:4.99')
    depends_on('qwt@6.0.1:')
    depends_on('mesa-glu')
    depends_on('glew')
    # GDAL's OGRSFDriverRegistrar is not compatible anymore starting with 2.0.
    depends_on('gdal@1.3.2:1.99')
    depends_on('cgal@3.5:')
    depends_on('proj@4.6.0:')
    # Boost's Python library has a different name starting with 1.67.
    # There were changes to Boost's optional in 1.61 that make the build fail.
    depends_on('boost+python@1.34:1.60')
    depends_on('python@2:2.99')

    # Officially, GPlates only supports GCC 4. Moreover, it requires
    # QtXmlPatterns, which Qt 4 only builds with GCC 4.
    conflicts('%gcc@5:')

    # When built in parallel, headers are not generated before they are used
    # (specifically, ViewportWindowUi.h).
    parallel = False

    def url_for_version(self, version):
        url = 'https://sourceforge.net/projects/gplates/files/gplates/{0}/gplates-{1}-unixsrc.tar.bz2/download'
        return url.format(version.up_to(2), version)

    def patch(self):
        # GPlates overrides FindPythonLibs and finds the static library, which
        # can not be used easily. Fall back to CMake's version, which finds
        # the shared library instead.
        force_remove('cmake/modules/FindPythonLibs.cmake')

        # GPlates only installs its binary for the Release configuration.
        filter_file('CONFIGURATIONS release',
                    'CONFIGURATIONS Debug Release RelWithDebInfo MinSizeRel',
                    'src/CMakeLists.txt')
