# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bolt(CMakePackage):
    """BOLT targets a high-performing OpenMP implementation,
    especially specialized for fine-grain parallelism. Unlike other
    OpenMP implementations, BOLT utilizes a lightweight threading
    model for its underlying threading mechanism. It currently adopts
    Argobots, a new holistic, low-level threading and tasking runtime,
    in order to overcome shortcomings of conventional OS-level
    threads. The current BOLT implementation is based on the OpenMP
    runtime in LLVM, and thus it can be used with LLVM/Clang, Intel
    OpenMP compiler, and GCC."""

    homepage = "http://www.bolt-omp.org/"
    url      = "https://github.com/pmodels/bolt/releases/download/v1.0b1/bolt-1.0b1.tar.gz"
    git      = "https://github.com/pmodels/bolt.git"

    version("master", branch="master")
    version("1.0rc1", "77733ba2ad9440c29b36d1c1411a9793")
    version("1.0b1", "df76beb3a7f13ae2dcaf9ab099eea87b")

    depends_on('argobots')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DLIBOMP_USE_ITT_NOTIFY=off',
            '-DLIBOMP_USE_ARGOBOTS=on',
            '-DLIBOMP_ARGOBOTS_INSTALL_DIR=' + spec['argobots'].prefix
        ]

        return options
