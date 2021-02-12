# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nettle(AutotoolsPackage, GNUMirrorPackage):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "https://www.lysator.liu.se/~nisse/nettle/"
    gnu_mirror_path = "nettle/nettle-3.3.tar.gz"

    version('3.7',   sha256='f001f64eb444bf13dd91bceccbc20acbc60c4311d6e2b20878452eb9a9cec75a')
    version('3.6',   sha256='d24c0d0f2abffbc8f4f34dcf114b0f131ec3774895f3555922fe2f40f3d5e3f1')
    version('3.5.1', sha256='75cca1998761b02e16f2db56da52992aef622bf55a3b45ec538bc2eedadc9419')
    version('3.5',   sha256='432d98dcd341cbd063a963025524122368c1f2ee9c721bb68d771d5e34674b4f')
    version('3.4.1', sha256='f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad')
    version('3.4',   sha256='ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94')
    version('3.3',   sha256='46942627d5d0ca11720fec18d81fc38f7ef837ea4197c1f630e71ce0d470b11e')
    version('3.2',   sha256='ea4283def236413edab5a4cf9cf32adf540c8df1b9b67641cfc2302fca849d97')
    version('2.7.1', sha256='bc71ebd43435537d767799e414fce88e521b7278d48c860651216e1fc6555b40')
    version('2.7',   sha256='c294ea133c05382cc2effb1734d49f4abeb1ad8515543a333de49a11422cd4d6')

    depends_on('gmp')
    depends_on('m4', type='build')

    def configure_args(self):
        return ['CFLAGS={0}'.format(self.compiler.c99_flag)]
