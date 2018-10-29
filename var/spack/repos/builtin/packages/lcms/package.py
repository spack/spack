# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lcms(AutotoolsPackage):
    """Little cms is a color management library. Implements fast
       transforms between ICC profiles. It is focused on speed, and is
       portable across several platforms (MIT license)."""

    homepage = "http://www.littlecms.com"
    url      = "http://downloads.sourceforge.net/project/lcms/lcms/2.9/lcms2-2.9.tar.gz"

    version('2.9', '8de1b7724f578d2995c8fdfa35c3ad0e')
    version('2.8', '87a5913f1a52464190bb655ad230539c')
    version('2.6', 'f4c08d38ceade4a664ebff7228910a33')

    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('zlib')
