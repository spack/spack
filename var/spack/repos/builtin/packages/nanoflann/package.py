# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nanoflann(CMakePackage):
    """a C++ header-only library for Nearest Neighbor (NN) search wih KD-trees.
    """

    homepage = "https://github.com/jlblancoc/nanoflann"
    url      = "https://github.com/jlblancoc/nanoflann/archive/v1.2.3.tar.gz"

    version('1.2.3', '92a0f44a631c41aa06f9716c51dcdb11')

    def patch(self):
        if self.spec.target.family == 'aarch64' and \
                self.spec.satisfies('%gcc@:5.9'):
            filter_file('-mtune=native', '', 'CMakeLists.txt')

    def cmake_args(self):
        args = ['-DBUILD_SHARED_LIBS=ON']
        return args
