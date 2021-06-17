# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Folly(CMakePackage):
    """Folly (acronymed loosely after Facebook Open Source Library) is a
    library of C++11 components designed with practicality and efficiency
    in mind.

    Folly contains a variety of core library components used extensively at
    Facebook. In particular, it's often a dependency of Facebook's other open
    source C++ efforts and place where those projects can share code.
    """

    homepage = "https://github.com/facebook/folly"
    url = "https://github.com/facebook/folly/releases/download/v2021.05.24.00/folly-v2021.05.24.00.tar.gz"
    

    version('2021.05.24.00', sha256='9d308adefe4670637f5c7d96309b3b394ac3fa129bc954f5dfbdd8b741c02aad')
    # TODO: Further versions below require testing, or removal
    # version('2017.06.05.00', sha256='d22ceda4dfe33583828be1193fa3929d70c51998f0797236e293c44ef828c6d0')
    # version('2016.11.14.00', sha256='cde5b3e1a38d181f7c4e52d590de1c1aca58da7b27b3020d08e9aa45b4c3ed74')
    # version('2016.11.07.00', sha256='4400d7f0fead90d88ce4caee9f0e9aeb8008c9954ea9034e19ae7226175206ba')
    # version('2016.10.31.00', sha256='7bef9ee956248f68f1c4e96be67561842ee6cc030a58e132b93b9be57b6b29ea')
    # version('2016.10.24.00', sha256='d54b609d3750a6a1cfbda7c62e1457af60cf5efc48d7a8e6552d67909e064757')
    # version('2016.10.17.00', sha256='0f83685016d020111ba54ddc48c0cf33e1e0b9b35cee5ae82d5f2cbc5f6b0e82')


    # CMakePackage Dependency
    depends_on('pkgconfig', type='build')

    # folly requires gcc 4.9+ and a version of boost compiled with C++14 support or higher
    # TODO: Specify the boost components
    variant('cxxstd', default='14', values=('14', '17'), multi=False, description='Use the specified C++ standard when building.')
    depends_on('boost+context cxxstd=14', when='cxxstd=14')
    depends_on('boost+context cxxstd=17', when='cxxstd=17')

    # required dependencies
    depends_on('gflags')
    depends_on('glog')
    depends_on('double-conversion')
    depends_on('libevent')
    depends_on('fmt')

    # TODO: optional dependencies
    variant('libdwarf', default=False, description="Optional Dependency")
    variant('elfutils', default=False, description="Optional Dependency")
    variant('libunwind', default=False, description="Optional Dependency")
    depends_on('libdwarf', when='+libdwarf')
    depends_on('elfutils', when='+elfutils')
    depends_on('libunwind', when='+libunwind')

    configure_directory = 'folly'
