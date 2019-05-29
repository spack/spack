# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libspatialite(AutotoolsPackage):
    """SpatiaLite is an open source library intended to extend the
       SQLite core to support fully fledged Spatial SQL capabilities."""

    homepage = "http://www.gaia-gis.it"
    url      = "http://www.gaia-gis.it/gaia-sins/libspatialite-4.3.0a.tar.gz"

    version('4.3.0a', '6b380b332c00da6f76f432b10a1a338c')

    depends_on('sqlite')
    depends_on('proj')
    depends_on('geos')
    depends_on('freexl')
