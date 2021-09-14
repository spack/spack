# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class Ccache(CMakePackage):
    """ccache is a compiler cache. It speeds up recompilation by caching
    previous compilations and detecting when the same compilation is being done
    again."""

    homepage = "https://ccache.dev/"
    url      = "https://github.com/ccache/ccache/releases/download/v4.2.1/ccache-4.2.1.tar.gz"
    maintainers = ['haampie']

    executables = ['^ccache$']

    version('4.4',   sha256='61a993d62216aff35722a8d0e8ffef9b677fc3f6accd8944ffc2a6db98fb3142')
    version('4.3',   sha256='b9789c42e52c73e99428f311a34def9ffec3462736439afd12dbacc7987c1533')
    version('4.2.1', sha256='320d2b17d2f76393e5d4bb28c8dee5ca783248e9cd23dff0654694d60f8a4b62')
    version('4.2',   sha256='dbf139ff32031b54cb47f2d7983269f328df14b5a427882f89f7721e5c411b7e')
    version('4.1',   sha256='cdeefb827b3eef3b42b5454858123881a4a90abbd46cc72cf8c20b3bd039deb7')
    version('4.0',   sha256='ac97af86679028ebc8555c99318352588ff50f515fc3a7f8ed21a8ad367e3d45')
    version('3.7.11', sha256='34309a59d4b6b6b33756366aa9d3144a4655587be9f914476b4c0e2d36365f01')
    version('3.7.9', sha256='92838e2133c9e704fdab9ee2608dad86c99021278b9ac47d065aa8ff2ea8ce36')
    version('3.7.1', sha256='e562fcdbe766406b6fe4bf97ce5c001d2be8a17465f33bcddefc9499bbb057d8')
    version('3.3.4', sha256='1348b54e7c35dd2f8d17923389e03c546e599cfbde6459d2f31cf6f1521ec538')
    version('3.3.3', sha256='87a399a2267cfac3f36411fbc12ff8959f408cffd050ad15fe423df88e977e8f')
    version('3.3.2', sha256='bf4a150dea611a206a933e122bd545dd6c5111d319505e0e30fef75f88651847')
    version('3.3.1', sha256='4101f9937cd6e8f50d0a5882f7e9a7312ba42c01ff41e4f359c94ae2c9b87879')
    version('3.3',   sha256='b220fce435fe3d86b8b90097e986a17f6c1f971e0841283dd816adb238c5fd6a')
    version('3.2.9', sha256='1e13961b83a3d215c4013469c149414a79312a22d3c7bf9f946abac9ee33e63f')

    depends_on('zstd', when='@4.0:')

    depends_on('gperf', when='@:3.99')
    depends_on('hiredis@0.13.3:', when='@4.4:')
    depends_on('libxslt', when='@:3.99')
    depends_on('zlib', when='@:3.99')

    conflicts('%gcc@:5', when='@4.4:')
    conflicts('%clang@:4', when='@4.4:')

    # Before 4.0 this was an Autotools package
    @when('@:3.99')
    def cmake(self, spec, prefix):
        configure_args = ["--prefix=" + prefix]
        configure(*configure_args)

    @when('@:3.99')
    def build(self, spec, prefix):
        make()

    @when('@:3.99')
    def install(self, spec, prefix):
        make("install")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'ccache.*version\s+(\S+)', output)
        return match.group(1) if match else None
