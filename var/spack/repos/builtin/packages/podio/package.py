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
    version('0.10.0', sha256='b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2')
    version('0.9.2', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240')
    version('0.9.0', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('0.8.0', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    # cpack config throws an error on some systems
    patch('cpack.patch', when="@:0.10.0")

    depends_on('root@6.08.06:')

    depends_on('cmake@3.8:', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s'
                    % self.spec['root'].variants['cxxstd'].value)
        args.append('-DBUILD_TESTING=%s' % self.run_tests)
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('PODIO', self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('PODIO', self.prefix)

    def url_for_version(self, version):
        # podio releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        major = (str(version[0]).zfill(2))
        minor = (str(version[1]).zfill(2))
        patch = (str(version[2]).zfill(2))
        if version[2] == 0:
            url = "https://github.com/AIDASoft/podio/archive/v%s-%s.tar.gz" % (major, minor)
        else:
            url = "https://github.com/AIDASoft/podio/archive/v%s-%s-%s.tar.gz" % (major, minor, patch)
        return url
