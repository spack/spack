# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Stc(AutotoolsPackage):
    """STC: The Swift-Turbine Compiler"""

    homepage = 'http://swift-lang.org/Swift-T'
    url      = 'http://swift-lang.github.io/swift-t-downloads/spack/stc-0.0.0.tar.gz'
    git      = "https://github.com/swift-lang/swift-t.git"

    version('master', branch='master')
    version('0.8.3', '1d7eee78d3531b7c1901c5aec5703721')
    version('0.8.2', '883b0657f1aac9b81158ef0a8989be4c')

    depends_on('java', type=('build', 'run'))
    depends_on('ant', type='build')
    depends_on('turbine', type=('build', 'run'))
    depends_on('turbine@master', type=('build', 'run'), when='@master')
    depends_on('zsh', type=('build', 'run'))
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    @when('@master')
    def configure_directory_helper(self):
        return "stc/code"

    @when('@0')
    def configure_directory_helper(self):
        return "."

    @property
    def configure_directory(self):
        return self.configure_directory_helper()

    def configure_args(self):
        args = ['--with-turbine=' + self.spec['turbine'].prefix]
        return args
