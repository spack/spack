# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class GtkDoc(AutotoolsPackage):
    """GtkDoc is a tool used to extract API documentation from
    C-code like Doxygen, but handles documentation of GObject
    (including signals and properties) that makes it very
    suitable for GTK+ apps and libraries. It uses docbook for
    intermediate files and can produce html by default and
    pdf/man-pages with some extra work."""

    homepage = "https://wiki.gnome.org/DocumentationProject/GtkDoc"
    url = "https://download.gnome.org/sources/gtk-doc/1.33/gtk-doc-1.33.2.tar.xz"
    list_url = "https://download.gnome.org/sources/gtk-doc/"
    list_depth = 1

    license("GPL-2.0-or-later AND GFDL-1.1-or-later")

    version("1.33.2", sha256="cc1b709a20eb030a278a1f9842a362e00402b7f834ae1df4c1998a723152bf43")
    version("1.32", sha256="de0ef034fb17cb21ab0c635ec730d19746bce52984a6706e7bbec6fb5e0b907c")

    # Commented out until package dblatex has been created
    # variant('pdf', default=False, description='Adds PDF support')

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("itstool", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig@0.19:", type=("build", "run"))

    depends_on("python@3.2:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-anytree", type=("test"))
    depends_on("py-lxml", type=("test"))
    depends_on("py-parameterized", type=("test"))
    depends_on("py-six", type=("test"))
    depends_on("libxslt")
    depends_on("libxml2@2.3.6:")
    depends_on("docbook-xsl")
    depends_on("docbook-xml")
    # depends_on('dblatex', when='+pdf')

    patch("build.patch")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        """If test/tools.sh does not find gtkdocize it starts a sh which blocks"""
        env.prepend_path("PATH", join_path(self.stage.source_path, "buildsystems", "autotools"))

    def install(self, spec, prefix):
        make("install", "V=1")
        install(join_path("buildsystems", "autotools", "gtkdocize"), prefix.bin)

    def installcheck(self):
        """gtk-doc does not support installcheck properly, skip it"""
        pass

    def url_for_version(self, version):
        url = "https://download.gnome.org/sources/gtk-doc/{0}/gtk-doc-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = ["--with-xml-catalog={0}".format(self["docbook-xml"].catalog)]
        return args
