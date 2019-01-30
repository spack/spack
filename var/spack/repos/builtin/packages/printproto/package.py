# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Printproto(AutotoolsPackage):
    """Xprint extension to the X11 protocol - a portable, network-transparent
    printing system."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/printproto"
    url      = "https://www.x.org/archive/individual/proto/printproto-1.0.5.tar.gz"

    version('1.0.5', '5afeb3a7de8a14b417239a14ea724268')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
