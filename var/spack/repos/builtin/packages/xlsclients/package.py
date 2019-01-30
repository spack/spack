# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xlsclients(AutotoolsPackage):
    """xlsclients is a utility for listing information about the client
    applications running on a X11 server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlsclients"
    url      = "https://www.x.org/archive/individual/app/xlsclients-1.1.3.tar.gz"

    version('1.1.3', '093c748d98b61dbddcaf3de1740fbd26')

    depends_on('libxcb@1.6:', when='@1.1:')
    depends_on('libx11', when='@:1.0')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
