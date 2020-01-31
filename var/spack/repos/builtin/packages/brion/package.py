# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *

class Brion(CMakePackage):
    """Blue Brain C++ File IO Library"""

    homepage = "https://github.com/BlueBrain/Brion"
    git = "https://github.com/BlueBrain/Brion.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('3.0.0', tag='3.0.0', submodules=True)
    version('3.1.0', tag='3.1.0', submodules=True, preferred=True)

    variant('python', default=False, description='Build Python wrapping')
    variant('doc', default=False, description='Build documentation')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('doxygen', type='build')

    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('py-numpy', type=('build', 'run'), when='+python')

    depends_on('boost +shared', when='~python')
    depends_on('boost +shared +python', when='+python')

    depends_on('libsonata ~mpi', when='@3.1.0:')

    # TODO: bzip2 is a dependency of boost. Needed here because of linking
    # issue (libboost_iostreams.so.1.68.0 not finding libbz2.so)
    depends_on('bzip2')
    depends_on('lunchbox')
    depends_on('vmmlib')
    depends_on('highfive@2.1: +boost ~mpi')
    depends_on('mvdtool ~mpi')

    def cmake_args(self):
        args = ['-DDISABLE_SUBPROJECTS=ON']

        if self.spec.satisfies('@3.1.0:'):
            args.append('-DEXTLIB_FROM_SUBMODULES=ON')

        return args

    @when('+python')
    def setup_run_environment(self, env):
        site_dir = self.spec['python'].package.site_packages_dir.split(os.sep)[1:]
        for target in (self.prefix.lib, self.prefix.lib64):
            pathname = os.path.join(target, *site_dir)
            if os.path.isdir(pathname):
                env.prepend_path('PYTHONPATH', pathname)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            ninja()
            if '+doc' in self.spec:
                ninja('doxygen', 'doxycopy')
