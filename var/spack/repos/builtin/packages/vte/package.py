# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vte(AutotoolsPackage):
    """The VTE package contains a termcap file implementation
    for terminal emulators"""

    homepage = "http://www.linuxfromscratch.org/blfs/view/svn/gnome/vte.html"
    url      = "http://ftp.gnome.org/pub/gnome/sources/vte/0.28/vte-0.28.2.tar.xz"
    _urlfmt  = "http://ftp.gnome.org/pub/gnome/sources/vte/{0}/vte-{1}.tar.xz"
    version('0.54.2', '054a8a46b9de9078f81931311cf27a68')
    version('0.36.5', '96f102ef9e178b6238edcfdb1fa9dbcc')
    version('0.36.2', '9c13f35f47b31abed4cdca2684d3d2ff')
    version('0.29.1', '91cd70995099ca7e534654e0679ab5a7')
    version('0.28.2', '497f26e457308649e6ece32b3bb142ff')

    depends_on('binutils', type='build')
    depends_on('libtool', type='build')
    depends_on('intltool', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('perl', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('gtkplus')
    depends_on('gtkplus@3.1:', when='@0.29:')
    depends_on('glib')

    def url_for_version(self, version):
        """Handle vte version-based custom URLs."""
        return self._urlfmt.format(version.up_to(2), version)

    def configure_args(self):
        # A hack to patch config.guess and config.sub
        # in the gnome-pty-helper sub directory
        copy('./config.guess', 'gnome-pty-helper/config.guess')
        copy('./config.sub', 'gnome-pty-helper/config.sub')
        return []
