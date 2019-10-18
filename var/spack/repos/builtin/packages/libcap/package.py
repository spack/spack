# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcap(MakefilePackage):
    """Libcap implements the user-space interfaces to the POSIX 1003.1e
    capabilities available in Linux kernels. These capabilities are a
    partitioning of the all powerful root privilege into a set of
    distinct privileges."""

    homepage = "https://sites.google.com/site/fullycapable/"
    url      = "https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-2.25.tar.xz"

    version('2.27', sha256='dac1792d0118bee6aae6ba7fb93ff1602c6a9bda812fd63916eee1435b9c486a')
    version('2.26', sha256='b630b7c484271b3ba867680d6a14b10a86cfa67247a14631b14c06731d5a458b')
    version('2.25', sha256='693c8ac51e983ee678205571ef272439d83afe62dd8e424ea14ad9790bc35162')

    patch('libcap-fix-the-libcap-native-building-failure-on-CentOS-6.7.patch', when="@2.25")

    def install(self, spec, prefix):
        make_args = [
            'RAISE_SETFCAP=no',
            'lib=lib',
            'prefix={0}'.format(prefix),
            'install'
        ]
        make(*make_args)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.lib, 'libcap.so'))
