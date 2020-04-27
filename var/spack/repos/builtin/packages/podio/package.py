# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Podio(CMakePackage):
    """PODIO, or plain-old-data I/O, is a C++ library to support the creation
    and handling of data models in particle physics."""

    homepage = "https://github.com/AIDASoft/podio"
    url      = "https://github.com/AIDASoft/podio/archive/v00-09-02.tar.gz"
    git      = "https://github.com/AIDASoft/podio.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    version('master', branch='master')
    version('00-10', sha256='b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2')
    version('00-09-02', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240')
    version('00-09', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('00-08', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    _cxxstd_values = ('14', '17')
    for s in _cxxstd_values:
        depends_on('root@6.08.06: cxxstd=' + s, when='cxxstd=' + s)

    depends_on('cmake', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s'
                    % self.spec.variants['cxxstd'].value)
        args.append('-DBUILD_TESTING=OFF')
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('PODIO', self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('PODIO', self.prefix)
