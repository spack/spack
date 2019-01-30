# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Thrust(Package):
    """Thrust is a parallel algorithms library
    which resembles the C++ Standard Template Library (STL)."""

    homepage = "https://thrust.github.io"
    url      = "https://github.com/thrust/thrust/archive/1.8.2.tar.gz"

    version('1.8.2', 'fc7fc807cba98640c816463b511fb53f')

    def install(self, spec, prefix):
        install_tree('doc', join_path(prefix, 'doc'))
        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('thrust', join_path(prefix, 'include', 'thrust'))
