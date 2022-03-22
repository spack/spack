# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Autodiff(CMakePackage):
    """autodiff is automatic differentiation made easier for C++."""

    homepage = "https://autodiff.github.io"
    url      = "https://github.com/autodiff/autodiff/archive/refs/tags/v0.6.4.tar.gz"
    list_url = "https://github.com/autodiff/autodiff/releases"
    git      = "https://github.com/autodiff/autodiff.git"

    maintainers = ['wdconinc', 'HadrienG2']

    version('0.6.4',  sha256='cfe0bb7c0de10979caff9d9bfdad7e6267faea2b8d875027397486b47a7edd75')
    version('0.5.13', sha256='a73dc571bcaad6b44f74865fed51af375f5a877db44321b5568d94a4358b77a1')

    variant('python', default='False', description='Enable the compilation of the python bindings.')
    variant('examples', default='False', description='Enable the compilation of the example files.')

    depends_on('cmake@3.0:', type='build')
    depends_on('eigen')
    depends_on('py-pybind11', type=('build', 'run'))

    def cmake_args(self):
        args = [
            self.define('AUTODIFF_BUILD_TESTS', self.run_tests),
            self.define_from_variant('AUTODIFF_BUILD_PYTHON', 'python'),
            self.define_from_variant('AUTODIFF_BUILD_EXAMPLES', 'examples',)
        ]
        return args
