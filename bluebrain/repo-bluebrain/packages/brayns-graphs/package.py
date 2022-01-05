# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BraynsGraphs(CMakePackage):
    """Brayns plugin"""
    homepage = "https://github.com/favreau/Brayns-UC-Graphs.git"
    git = "https://github.com/favreau/Brayns-UC-Graphs.git"

    generator = 'Ninja'

    version('develop')
    version('0.1.0', tag='0.1.0')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brayns@1:')
