# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    version('0.6.3',  sha256='afcc21c74c9c20ecf08c53ab82965652438d5bb65d146a2db43795b051c12135')
    version('0.6.2',  sha256='b065ac0ec4a94763567a3e7bd79a7d88f464a2028957bfcb994b923a0917c5e6')
    version('0.6.1',  sha256='b2e8ed18ee6eb39cac9232f8cd0c29b9cd08a236417740361f5ac46118bf9374')
    version('0.6.0',  sha256='b76e6a96e539f173a2a24eefa6f4e7cff54b1144cc51c51eba44ac3779a14013')
    version('0.5.13', sha256='a73dc571bcaad6b44f74865fed51af375f5a877db44321b5568d94a4358b77a1')
    version('0.5.12', sha256='f4d9648cc44a0016580c3e970e0a642c49225f5ff51fd41233bfa4db8681f460')
    version('0.5.11', sha256='d6c5a7ea5459c98bfd2b6fd34a883b78ef1372e3e35ae07cd40fdf7c4a5c7576')
    version('0.5.10', sha256='d0e62994b7984014b2944d13f6ce9a75fc6b681d2d81f9051ec44410912dc5d7')
    version('0.5.9',  sha256='c746bf611c66acc94113aa4483caf73631216d6db5b511df2b5dcb29a0a4345a')

    variant('python', default='False', description='Enable the compilation of the python bindings.')
    variant('examples', default='False', description='Enable the compilation of the example files.')
    variant('docs', default='False', description='Enable the build of the documentation and website.')

    depends_on('cmake@3.0:', type='build')
    depends_on('eigen')
    depends_on('py-pybind11', type=('build', 'run'))
    # FIXME no py-mkdocs yet in spack
    #depends_on('py-mkdocs', when='+docs')
    conflicts('+docs', msg='No support yet for py-mkdocs in spack')

    def cmake_args(self):
        args = [
            self.define('AUTODIFF_BUILD_TESTS',self.run_tests),
            self.define_from_variant('AUTODIFF_BUILD_PYTHON', 'python'),
            self.define_from_variant('AUTODIFF_BUILD_EXAMPLES', 'examples',),
            self.define_from_variant('AUTODIFF_BUILD_DOCS', 'docs')
        ]
        return args
