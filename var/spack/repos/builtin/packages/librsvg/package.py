# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Librsvg(AutotoolsPackage):
    """Library to render SVG files using Cairo"""

    homepage = "https://wiki.gnome.org/Projects/LibRsvg"
    url      = "https://download.gnome.org/sources/librsvg/2.44/librsvg-2.44.14.tar.xz"

    version('2.44.14', sha256='6a85a7868639cdd4aa064245cc8e9d864dad8b8e9a4a8031bb09a4796bc4e303')

    depends_on("gobject-introspection", type='build')
    depends_on("pkgconfig", type='build')
    depends_on("rust", type='build')
    depends_on("cairo")
    depends_on("gdk-pixbuf")
    depends_on("glib")
    depends_on("libcroco")
    depends_on("pango")
    depends_on('libffi')
    depends_on('libxml2')

    def url_for_version(self, version):
        url  = "https://download.gnome.org/sources/librsvg"
        url += "{0}/librsvg-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
