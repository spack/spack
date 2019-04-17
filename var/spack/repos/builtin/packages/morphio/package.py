# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Morphio(CMakePackage):
    """Library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO"
    url      = "https://github.com/BlueBrain/MorphIO.git"

    version('develop', git=url, submodules=True)
    version('2.0.8', tag='v2.0.8', git=url, submodules=True, preferred=True)

    depends_on('cmake@3.2:', type='build')
    depends_on('hdf5')

    def cmake_args(self):
        args = ['-DBUILD_BINDINGS:BOOL=OFF']
        return args
