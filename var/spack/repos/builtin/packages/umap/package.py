# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Umap(CMakePackage):
    """Umap is a library that provides an mmap()-like interface to a
    simple, user-space page fault handler based on the userfaultfd Linux
    feature (starting with 4.3 linux kernel)."""

    homepage = "https://github.com/LLNL/umap"
    url      = "https://github.com/LLNL/umap/archive/v2.1.0.tar.gz"
    git      = "https://github.com/LLNL/umap.git"

    tags = ['e4s']

    maintainers = ['egreen77', 'ibpeng', 'mayagokhale']

    version('develop', branch='develop')
    version('2.1.0', sha256='dfdc5b717aecdbfbb0da22e8567b9f2ffbc3607000a31122bf7c5ab3b85cecd9')
    version('2.0.0', sha256='85c4bc68e8790393847a84eb54eaf6fc321acade382a399a2679d541b0e34150')
    version('1.0.0', sha256='c746de3fae5bfc5bbf36234d5e888ea45eeba374c26cd8b5a817d0c08e454ed5')

    variant('logging', default=False, description='Build with logging enabled.')
    variant('tests', default=False, description='Build examples/tests.')
    variant('stats', default=False, description='Print internal stats when closing.')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_LOGGING', 'logging'),
            self.define_from_variant('ENABLE_TESTS', 'tests'),
            self.define_from_variant('ENABLE_DISPLAY_STATS', 'stats')
        ]
        return args
