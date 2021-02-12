# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tpm2Tss(AutotoolsPackage):
    """OSS implementation of the TCG TPM2 Software Stack (TSS2)"""

    homepage = "https://tpm2-software.github.io/"
    url      = "https://github.com/tpm2-software/tpm2-tss/archive/3.0.0.tar.gz"

    version('3.0.3', sha256='78392be7309baf47f51b122f566ac915fd4d1760ea78571cba2e1484f9b5be17')
    version('3.0.2', sha256='8f3b7ac8b7404a361013d1adb38be33f69384f2f9fbb44dabe94597f63ab0e00')
    version('3.0.1', sha256='2432533a1cac0f0d15d0337d2f0a23591a50b36aad68ab72412ce694818b7e76')
    version('3.0.0', sha256='e88e91aeee2e01ccc45596fb8afcc3b521a660dcebe5a6e1b14ea5e9e5c15cf5')
    version('2.4.2', sha256='1cec5e834a6a750b138cabcd100b3fcd12b16cd21fa4f9103739914743511f75')
    version('2.4.1', sha256='cc6f0691307f3c65d5a1375e2cd22508cc72850dbc70eb820b892f0b3d0cbea2')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('autoconf-archive', type='build')
    depends_on('json-c')
    depends_on('curl')
    depends_on('doxygen', type='build', when='@:2.4.2')
    depends_on('libgcrypt', when='@:2.4.2')

    @when('@:2.4.2')
    def setup_build_environment(self, env):
        env.prepend_path('ACLOCAL_PATH',
                         self.spec['libgcrypt'].prefix.share.aclocal)
        env.prepend_path('ACLOCAL_PATH',
                         self.spec['autoconf-archive'].prefix.share.aclocal)

    @when('@3.0.0:')
    def setup_build_environment(self, env):
        env.prepend_path('ACLOCAL_PATH',
                         self.spec['autoconf-archive'].prefix.share.aclocal)

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('./bootstrap')
