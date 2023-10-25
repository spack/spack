# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Acl(AutotoolsPackage):
    """Commands for Manipulating POSIX Access Control Lists."""

    homepage = "https://savannah.nongnu.org/projects/acl"
    url = "https://git.savannah.nongnu.org/cgit/acl.git/snapshot/acl-2.3.1.tar.gz"

    maintainers("cosmicexplorer")

    version("2.3.1", sha256="8cad1182cc5703c3e8bf7a220fc267f146246f088d1ba5dd72d8b02736deedcc")
    version("2.3.0", sha256="3659cf37ca29c0493f7d692d81dba5e1032b966d14674b6f0d637ff92afca4be")
    version("2.2.53", sha256="9e905397ac10d06768c63edd0579c34b8431555f2ea8e8f2cee337b31f856805")
    version("2.2.52", sha256="f3f31d2229c903184ff877aa0ee658b87ec20fec8aebb51e65eaa68d7b24e629")
    version("2.2.51", sha256="31a43d96a274a39bfcb805fb903d45840515344884d224cef166b482693a9f48")
    version("2.2.50", sha256="39e21d623a9f0da8c042cde346c01871b498d51400e92c2ab1490d5ffd724401")
    version("2.2.49", sha256="c6e01460cac4e47673dd60a7f57b970b49f6998bb564eff141cca129aa8940d1")
    version("2.2.48", sha256="877eaeccc1500baec58391935b46ac7dfc5ffd8c54fbc0385ccd8b2b18ac3fa6")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("bash", type="build")
    depends_on("gettext")

    depends_on("attr")
    # The configure step fails to find attr/xattr.h for these versions of acl unless this exact
    # version of attr is used.
    depends_on("attr@2.4.47", when="@:2.2.51")

    # In 2.2.53 and later, the codebase provides a nice autogen script.
    @when("@2.2.53:")
    def autoreconf(self, spec, prefix):
        which("bash")("./autogen.sh")

    # Before 2.2.53, the project's script to generate ./configure was contained in a Makefile which
    # both generated the ./configure file and then executed a hardcoded ./configure command line
    # with hardcoded install prefixes pointing to / and /usr. This patch removes the
    # "make configure" target and replaces it with a "make autoconf" target that stops after
    # generating the ./configure script, allowing spack to take over afterwards.
    patch("makefile-autoconf-only.patch", when="@:2.2.52")

    @when("@:2.2.52")
    def autoreconf(self, spec, prefix):
        make("autoconf")

    def flag_handler(self, name, flags):
        if name == "ldlibs" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        # For some reason, self.build_system_flags(...) fails to link libintl, and results in link
        # errors for functions in that library. self.inject_flags(...) seems to fix this.
        return self.inject_flags(name, flags)
