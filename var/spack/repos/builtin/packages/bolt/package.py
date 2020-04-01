# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    maintainers = ['shintaro-iwasaki']

    version("master", branch="master")
    version("1.0rc3", sha256="beec522d26e74f0a562762ea5ae7805486a17b40013090ea1472f0c34c3379c8")
    version("1.0rc2", sha256="662ab0bb9583e8d733e8af62a97b41828e8bfe4bd65902f1195b986901775a45")
    version("1.0rc1", sha256="c08cde0695b9d1252ab152425be96eb29c70d764e3083e276c013804883a15a4")
    version("1.0b1", sha256="fedba46ad2f8835dd1cec1a9a52bcc9d8923071dc40045d0360517d09cd1a57d")

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
