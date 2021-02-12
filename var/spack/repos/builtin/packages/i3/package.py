# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class I3(AutotoolsPackage):
    """i3, improved tiling wm. i3 is a tiling window manager, completely
    written from scratch. The target platforms are GNU/Linux and BSD operating
    systems, our code is Free and Open Source Software (FOSS) under the BSD
    license. i3 is primarily targeted at advanced users and developers."""

    homepage = "https://i3wm.org/"
    url      = "https://github.com/i3/i3/archive/4.14.1.tar.gz"

    version('4.19.1', sha256='4cdf74981a9b54924a11f2c314a36a92cdbc4fac51390c4864a2ea63287cefc4')
    version('4.19',   sha256='acff3a1772e203207de08c4c4c89f376da1f9d08d5bb9964f4bab2bf03918879')
    version('4.18.3', sha256='03ccfd26a4afca444f6634901954f01002b57b65c578840f9d75dd83ddd5d6a8')
    version('4.18.2', sha256='83a7bf477fddff9f53011500fc315795d6ffc7eb7f2831062e032cb994436494')
    version('4.18.1', sha256='6a714c742096fa1cac22adb75b2cf8408d396b0a37dde688f48871b456f57b00')
    version('4.18',   sha256='3835b54389ff0e421771b57fdc1c6693c45173bb69026d87516401a773ad9d27')
    version('4.17.1', sha256='7a1984f2fc2680e34644388d08e64fa70aea8070af474c96717ad92d2499c5d9')
    version('4.17',   sha256='1653dc49a6e7f4cd03c51456e639b634e913e2bf21f6be674d93a7e3a930cf72')
    version('4.16.1', sha256='088a81002e5c17b1756e86d4db43dce56c81009f48ee455070668ea2ac09bafd')
    version('4.16',   sha256='2c25c4ab099a27560904fb9468a6024f15757d1ff4af512fb4ab10c205a6dbce')
    version('4.14.1', sha256='28d8102d656f17445a6e1523b12c1a730cc3925a520add1f75b56b9c842932f9')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libev')
    depends_on('startup-notification')
    depends_on('xcb-util-cursor')
    depends_on('xcb-util-keysyms')
    depends_on('xcb-util-wm')
    depends_on('xcb-util-xrm')
    depends_on('libxkbcommon')
    depends_on('yajl')
    depends_on('cairo+X')
    depends_on('pango+X')
