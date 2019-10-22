# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libspatialite(AutotoolsPackage):
    """SpatiaLite is an open source library intended to extend the
       SQLite core to support fully fledged Spatial SQL capabilities."""

    homepage = "http://www.gaia-gis.it"
    url      = "http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0a.tar.gz"

    version('4.3.0a', sha256='88900030a4762904a7880273f292e5e8ca6b15b7c6c3fb88ffa9e67ee8a5a499')
    version('3.0.1', sha256='4983d6584069fd5ff0cfcccccee1015088dab2db177c0dc7050ce8306b68f8e6')

    depends_on('pkg-config', type='build')
    depends_on('sqlite+rtree')
    depends_on('proj@:5')
    depends_on('geos')
    depends_on('freexl')
    depends_on('libiconv')
    depends_on('libxml2')
