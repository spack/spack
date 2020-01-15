# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icu4c(AutotoolsPackage):
    """ICU is a mature, widely used set of C/C++ and Java libraries providing
    Unicode and Globalization support for software applications. ICU4C is the
    C/C++ interface."""

    homepage = "http://site.icu-project.org/"
    url      = "https://github.com/unicode-org/icu/releases/download/release-65-1/icu4c-65_1-src.tgz"

    version('65.1', sha256='53e37466b3d6d6d01ead029e3567d873a43a5d1c668ed2278e253b683136d948')
    version('64.1', sha256='92f1b7b9d51b396679c17f35a2112423361b8da3c1b9de00aa94fd768ae296e6')
    version('60.1', sha256='f8f5a6c8fbf32c015a467972bdb1477dc5f5d5dfea908b6ed218715eeb5ee225')
    version('58.2', sha256='2b0a4410153a9b20de0e20c7d8b66049a72aef244b53683d0d7521371683da0c')
    version('57.1', sha256='ff8c67cb65949b1e7808f2359f2b80f722697048e90e7cfc382ec1fe229e9581')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building')

    depends_on('python', type='build', when='@64.1:')

    conflicts('%intel@:16', when='@60.1:',
              msg="Intel compilers have immature C++11 and multibyte support")

    configure_directory = 'source'

    def url_for_version(self, version):
        if version >= Version('65'):
            url = "https://github.com/unicode-org/icu/releases/download/release-{0}/icu4c-{1}-src.tgz"
            return url.format(version.dashed, version.underscored)
        else:
            url = "http://download.icu-project.org/files/icu4c/{0}/icu4c-{1}-src.tgz"
            return url.format(version.dotted, version.underscored)

    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            # Control of the C++ Standard is via adding the required "-std"
            # flag to CXXFLAGS in env
            flags.append(getattr(self.compiler,
                         'cxx{0}_flag'.format(
                             self.spec.variants['cxxstd'].value)))
        return (None, flags, None)

    # Need to make sure that locale is UTF-8 in order to process source
    # files in UTF-8.
    @when('@59:')
    def setup_build_environment(self, env):
        env.set('LC_ALL', 'en_US.UTF-8')

    def configure_args(self):
        args = []

        if 'python' in self.spec:
            # Make sure configure uses Spack's python package
            # Without this, configure could pick a broken global installation
            args.append('PYTHON={0}'.format(self.spec['python'].command))

        # The --enable-rpath option is only needed on MacOS, and it
        # breaks the build for xerces-c on Linux.
        if 'platform=darwin' in self.spec:
            args.append('--enable-rpath')

        return args
