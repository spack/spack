# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gconf(AutotoolsPackage):
    """GConf is a system for storing application preferences."""

    homepage = "https://projects.gnome.org/gconf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/GConf/3.2/GConf-3.2.6.tar.xz"

    version('3.2.6', sha256='1912b91803ab09a5eed34d364bf09fe3a2a9c96751fde03a4e0cfa51a04d784c')

    depends_on('glib@2.14.0:')
    depends_on('libxml2')

    # TODO: add missing dependencies
    # gio-2.0 >= 2.31.0
    # gthread-2.0
    # gmodule-2.0 >= 2.7.0
    # gobject-2.0 >= 2.7.0
    # dbus-1 >= 1.0.0
    # dbus-glib-1 >= 0.74
