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
    version('0.12.0', sha256='1729a2ce21e8b307fc37dfb9a9f5ae031e9f4be4992385cf99dba3e5fdf5323a')
    version('0.11.0', sha256='4b2765566a14f0ddece2c894634e0a8e4f42f3e44392addb9110d856f6267fb6')
    version('0.10.0', sha256='b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2')
    version('0.9.2', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240')
    version('0.9.0', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('0.8.0', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    # cpack config throws an error on some systems
    patch('cpack.patch', when="@:0.10.0")
    patch('dictloading.patch', when="@0.10.0")

    depends_on('root@6.08.06: cxxstd=17')

    depends_on('cmake@3.8:', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-jinja2@2.10.1:', type=('build', 'run'), when='@0.12.0:')

    def cmake_args(self):
        args = ['-DBUILD_TESTING=%s' % self.run_tests, ]
        return args

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
