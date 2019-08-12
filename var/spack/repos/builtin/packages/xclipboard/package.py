# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xclipboard(AutotoolsPackage):
    """xclipboard is used to collect and display text selections that are
    sent to the CLIPBOARD by other clients.  It is typically used to save
    CLIPBOARD selections for later use.  It stores each CLIPBOARD
    selection as a separate string, each of which can be selected."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xclipboard"
    url      = "https://www.x.org/archive/individual/app/xclipboard-1.1.3.tar.gz"

    version('1.1.3', 'cee91df9df1b5d63034681546fd78c0b')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.1:')
    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
