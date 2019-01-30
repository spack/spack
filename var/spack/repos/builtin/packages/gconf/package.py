# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gconf(AutotoolsPackage):
    """GConf is a system for storing application preferences."""

    homepage = "https://projects.gnome.org/gconf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/GConf/3.2/GConf-3.2.6.tar.xz"

    version('3.2.6', '2b16996d0e4b112856ee5c59130e822c')

    depends_on('glib@2.14.0:')
    depends_on('libxml2')

    # TODO: add missing dependencies
    # gio-2.0 >= 2.31.0
    # gthread-2.0
    # gmodule-2.0 >= 2.7.0
    # gobject-2.0 >= 2.7.0
    # dbus-1 >= 1.0.0
    # dbus-glib-1 >= 0.74
