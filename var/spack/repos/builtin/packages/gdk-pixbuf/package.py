# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GdkPixbuf(AutotoolsPackage):
    """The Gdk Pixbuf is a toolkit for image loading and pixel buffer
       manipulation. It is used by GTK+ 2 and GTK+ 3 to load and
       manipulate images. In the past it was distributed as part of
       GTK+ 2 but it was split off into a separate package in
       preparation for the change to GTK+ 3."""
    homepage = "https://developer.gnome.org/gdk-pixbuf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.31/gdk-pixbuf-2.31.2.tar.xz"
    list_url = "http://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/"
    list_depth = 2

    version('2.31.2', '6be6bbc4f356d4b79ab4226860ab8523')

    depends_on("pkgconfig", type="build")
    depends_on("gettext")
    depends_on("glib")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("gobject-introspection")

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)

    def configure_args(self):
        args = []
        # disable building of gtk-doc files following #9771
        args.append('--disable-gtk-doc-html')
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))
        return args
