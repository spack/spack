# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JsonGlib(AutotoolsPackage):
    """JSON-GLib is a library for reading and parsing JSON using GLib and
    GObject data types and API."""

    homepage = "https://developer.gnome.org/json-glib"
    url      = "https://ftp.gnome.org/pub/gnome/sources/json-glib/1.2/json-glib-1.2.8.tar.xz"

    version('1.2.8', 'ff31e7d0594df44318e12facda3d086e')

    depends_on('glib')
