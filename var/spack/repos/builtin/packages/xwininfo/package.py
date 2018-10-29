# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xwininfo(AutotoolsPackage):
    """xwininfo prints information about windows on an X server. Various
    information is displayed depending on which options are selected."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwininfo"
    url      = "https://www.x.org/archive/individual/app/xwininfo-1.1.3.tar.gz"

    version('1.1.3', 'd26623fe240659a320367bc453f1d301')

    depends_on('libxcb@1.6:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
