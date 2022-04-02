# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Libuv(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "https://libuv.org"
    url = "https://dist.libuv.org/dist/v1.44.1/libuv-v1.44.1-dist.tar.gz"

    version('1.44.1', sha256='b7293cefb470e17774dcf5d62c4c969636172726155b55ceef5092b7554863cc')
    version('1.44.0', sha256='6c52494401cfe8d08fb4ec245882f0bd4b1572b5a8e79d6c418b855422a1a27d')
    version('1.43.0', sha256='90d72bb7ae18de2519d0cac70eb89c319351146b90cd3f91303a492707e693a4')
    version('1.42.0', sha256='43129625155a8aed796ebe90b8d4c990a73985ec717de2b2d5d3a23cfe4deb72')
    version('1.41.1', sha256='65db0c7f2438bc8cd48865de282bf6670027f3557d6e3cb62fb65b2e350a687d')
    version('1.41.0', sha256='1184533907e1ddad9c0dcd30a5abb0fe25288c287ff7fee303fff7b9b2d6eb6e')
    version('1.40.0', sha256='61a90db95bac00adec1cc5ddc767ebbcaabc70242bd1134a7a6b1fb1d498a194')
    version('1.39.0', sha256='5c52de5bdcfb322dbe10f98feb56e45162e668ad08bc28ab4b914d4f79911697')
    version('1.38.1', sha256='0ece7d279e480fa386b066130a562ad1a622079d43d1c30731f2f66cd3f5c647')
    version('1.25.0', sha256='0e927ddc0f1c83899000a63e9286cac5958222f8fb5870a49b0c81804944a912')
    version('1.10.0', sha256='0307a0eec6caddd476f9cad39e18fdd6f22a08aa58103c4b0aead96d638be15e')
    version('1.9.0',  sha256='d595b2725abcce851c76239aab038adc126c58714cfb572b2ebb2d21b3593842')

    def url_for_version(self, version):
        if version < Version('1.44.0'):
            url = "https://dist.libuv.org/dist/v{0}/libuv-v{0}.tar.gz"
        else:
            url = "https://dist.libuv.org/dist/v{0}/libuv-v{0}-dist.tar.gz"
        return url.format(version, version)

    depends_on('automake', type='build', when='@:1.43.0')
    depends_on('autoconf', type='build', when='@:1.43.0')
    depends_on('libtool', type='build', when='@:1.43.0')
    depends_on('m4', type='build', when='@:1.43.0')

    # Tries to build an Objective-C file with GCC's C frontend
    # https://github.com/libuv/libuv/issues/2805
    conflicts('%gcc platform=darwin', when='@:1.37.9',
              msg='libuv does not compile with GCC on macOS yet, use clang. '
                  'See: https://github.com/libuv/libuv/issues/2805')

    @when('@:1.43')
    def autoreconf(self, spec, prefix):
        # This is needed because autogen.sh generates on-the-fly
        # an m4 macro needed during configuration
        Executable('./autogen.sh')()
