# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Cnpy(CMakePackage):
    """cnpy: library to read/write .npy and .npz files in C/C++."""

    homepage = "https://github.com/rogersce/cnpy"
    git      = "https://github.com/rogersce/cnpy.git"

    version('master', branch='master')

    def cmake_args(self):
        args = []
        if sys.platform == 'darwin':
            args.extend(['-DCMAKE_MACOSX_RPATH=ON'])

        return args
