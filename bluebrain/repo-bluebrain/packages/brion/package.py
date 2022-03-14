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
    version('3.1.0', tag='3.1.0', submodules=True)
    version('3.2.0', tag='3.2.0', submodules=True)
    version('3.3.0', tag='3.3.0', submodules=True)
    version('3.3.1', tag='3.3.1', submodules=True)
    version('3.3.2', tag='3.3.2', submodules=True)
    version('3.3.3', tag='3.3.3', submodules=True)
    version('3.3.4', tag='3.3.4', submodules=True)
    version('3.3.5', tag='3.3.5', submodules=False)
    version('3.3.6', tag='3.3.6', submodules=False)
    version('3.3.7', tag='3.3.7', submodules=False)
    version('3.3.8', tag='3.3.8', submodules=False)

    variant('python', default=False, description='Build Python wrapping')
    variant('doc', default=False, description='Build documentation')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('doxygen', type='build')

    depends_on('python@3.4:', type=('build', 'run'), when='+python')
    depends_on('py-numpy', type=('build', 'run', 'test'), when='+python')

    depends_on('boost +shared', when='~python')
    depends_on('boost +shared +python', when='+python')

    depends_on('libsonata@0.1.2', when='@:3.1.0')
    depends_on('libsonata', when='@3.2.0:')
    depends_on('morphio', when='@3.3.5:')

    # TODO: bzip2 is a dependency of boost. Needed here because of linking
    # issue (libboost_iostreams.so.1.68.0 not finding libbz2.so)
    depends_on('bzip2')
    depends_on('lunchbox', when='@3.1.0')
    depends_on('vmmlib', when='@3.1.0')
    depends_on('highfive@2.3.1 +boost', when='@3.3.8:')
    depends_on('highfive@2.2.2 +boost', when='@3.3.2:3.3.7')
    depends_on('highfive@2.2.1 +boost', when='@3.2.0:3.3.1')
    depends_on('highfive@2.1.1 +boost', when='@3.1.0')
    depends_on('mvdtool')
    depends_on('glm@:0.9.9.5')

    patch('https://patch-diff.githubusercontent.com/raw/BlueBrain/Brion/pull/334.patch',
          sha256='a1100b4581d424e3717bac1f5bf5682bd04b9e778213fb51014276b5b0d19bf9',
          when='@3.3.4 ^python@3.9:')

    def patch(self):
        if self.spec.version == Version('3.1.0'):
            filter_file(r'-py36', r'36 -py36',
                        'CMake/common/ChoosePython.cmake')
        if self.spec.satisfies('@3.2.0'):
            filter_file(r'-Werror', r'# -Werror',
                        'CMake/CompileOptions.cmake')
        elif self.spec.satisfies('@3.3.0:'):
            filter_file(
                r'-Werror',
                '-Werror -Wno-error=deprecated-copy -Wno-error=range-loop-construct '
                '-Wno-error=unused-function',
                'CMake/CompileOptions.cmake'
            )

    def cmake_args(self):
        args = ['-DBRION_SKIP_LIBSONATA_SUBMODULE=ON',
                '-DDISABLE_SUBPROJECTS=0N',
                '-DBRION_REQUIRE_PYTHON=%s' % ("ON" if "+python" in self.spec
                                               else "OFF")]
        if self.spec.satisfies('@3.1.0'):
            args.append('-DCOMMON_DISABLE_WERROR:BOOL=ON')
        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies('+python'):
            site_dir = self._get_site_dir()
            for target in (self.prefix.lib, self.prefix.lib64):
                pathname = os.path.join(target, *site_dir)
                if os.path.isdir(pathname):
                    env.prepend_path('PYTHONPATH', pathname)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            ninja()
            if '+doc' in self.spec:
                ninja('doxygen', 'doxycopy')

    @when('+python')
    @run_after('install')
    def test(self):
        site_dir = self._get_site_dir()
        for target in (self.prefix.lib, self.prefix.lib64):
            pathname = os.path.join(target, *site_dir)
            if os.path.isdir(pathname):
                with working_dir(pathname):
                    if self.spec.version >= Version('3.1.0') and \
                       self.spec.version <= Version('3.2.0'):
                        python('-c', 'import brain; print(brain)')
                    else:
                        python('-c', 'import brion; print(brion)')

    def _get_site_dir(self):
        return (self.spec['python']
                    .package.site_packages_dir.split(os.sep)[1:])
