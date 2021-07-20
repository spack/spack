# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class Shellcheck(Package):
    """ShellCheck is a GPLv3 tool that gives warnings and suggestions
    for bash/sh shell scripts"""

    homepage = "https://www.shellcheck.net"
    url      = "https://github.com/koalaman/shellcheck/releases/download/v0.7.2/shellcheck-v0.7.2.linux.x86_64.tar.xz"

    maintainers = ['ajkotobi']

    version('0.7.2', sha256='70423609f27b504d6c0c47e340f33652aea975e45f312324f2dbf91c95a3b188')
    version('0.7.1', sha256='64f17152d96d7ec261ad3086ed42d18232fcb65148b44571b564d688269d36c8')
    version('0.7.0', sha256='39c501aaca6aae3f3c7fc125b3c3af779ddbe4e67e4ebdc44c2ae5cba76c847f')
    version('0.6.0', sha256='95c7d6e8320d285a9f026b5241f48f1c02d225a1b08908660e8b84e58e9c7dce')
    version('0.5.0', sha256='7d4c073a0342cf39bdb99c32b4749f1c022cf2cffdfb080c12c106aa9d341708')
    version('0.4.7', sha256='deeea92a4d3a9c5b16ba15210d9c1ab84a2e12e29bf856427700afd896bbdc93')

    def url_for_version(self, version):
        url_arch = "https://github.com/koalaman/shellcheck/releases/download/v{0}/shellcheck-v{0}.{1}.{2}.tar.xz"
        return url_arch.format(version, platform.system(), platform.machine())

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('shellcheck', prefix.bin)
