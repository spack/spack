# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libspatialindex(CMakePackage):
    homepage = "http://libspatialindex.github.io"
    url      = "https://github.com/libspatialindex/libspatialindex/tarball/1.8.5"

    version('1.8.5', 'a95d8159714dbda9a274792cd273d298')
