# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelTbbOneapi(CMakePackage):
    """Widely used C++ template library for task parallelism.
    Intel Threading Building Blocks (Intel TBB) lets you easily write parallel
    C++ programs that take full advantage of multicore performance, that are
    portable and composable, and that have future-proof scalability.
    """
    homepage = "http://www.threadingbuildingblocks.org/"
    url_prefix = 'https://github.com/oneapi-src/oneTBB/'
    url = url_prefix + 'archive/v2020.1.tar.gz'

    # Note: when adding new versions, please check and update the
    # patches, filters and url_for_version() below as needed.
    version('2021.3.0',      sha256='8f616561603695bbb83871875d2c6051ea28f8187dbe59299961369904d1d49e')
    version('2021.2.0',      sha256='cee20b0a71d977416f3e3b4ec643ee4f38cedeb2a9ff015303431dd9d8d79854')
    version('2021.1.1',      sha256='b182c73caaaabc44ddc5ad13113aca7e453af73c1690e4061f71dfe4935d74e8')

    provides('tbb')

    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build and install CMake config files if we're new enough.
    depends_on('cmake@3.0.0:', type='build')
    depends_on('hwloc')

    # Version and tar file names:
    #  2020.0 --> v2020.0.tar.gz  starting with 2020
    #
    def url_for_version(self, version):
        url = self.url_prefix + 'archive/{0}.tar.gz'
        name = 'v{0}'.format(version)
        return url.format(name)

    def cmake_args(self):
        spec = self.spec
        options = []
        options.append('-DCMAKE_HWLOC_2_INCLUDE_PATH=%s' %
                       spec['hwloc'].prefix.include)
        options.append('-DCMAKE_HWLOC_2_LIBRARY_PATH=%s' %
                       spec['hwloc'].libs)
        options.append('-DTBB_CPF=ON')
        options.append('-DTBB_STRICT=OFF')
        if spec.variants['cxxstd'].value != 'default':
            options.append('-DCMAKE_CXX_STANDARD=%s' %
                           spec.variants['cxxstd'].value)
        return options
