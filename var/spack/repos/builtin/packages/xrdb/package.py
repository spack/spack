# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xrdb(AutotoolsPackage):
    """xrdb - X server resource database utility."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrdb"
    url      = "https://www.x.org/archive/individual/app/xrdb-1.1.0.tar.gz"

    version('1.1.0', 'd48983e561ef8b4b2e245feb584c11ce')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
