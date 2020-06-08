# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alps(CmakePackage):
    """Algorithms for Physics Simulations

    Keywords: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://alps.comp-phys.org"
    url      = "http://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"

    version('1.3.5', sha256='')

    depends_on('cmake@3.6.2')
    depends_on('python@3.5.2', type=('build', 'link', 'run'))
    depends_on('boost@1.63.0')
    depends_on('hdf5@1.8.17')
