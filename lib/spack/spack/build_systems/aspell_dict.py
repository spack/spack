# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs

import spack.directives
import spack.package_base
import spack.util.executable

from .autotools import AutotoolsBuilder, AutotoolsPackage


class AspellBuilder(AutotoolsBuilder):
    """The Aspell builder is close enough to an autotools builder to allow
    specializing the builder class, so to use variables that are specific
    to the Aspell extensions.
    """

    def configure(self, pkg, spec, prefix):
        aspell = spec["aspell"].prefix.bin.aspell
        prezip = spec["aspell"].prefix.bin.prezip
        destdir = prefix

        sh = spack.util.executable.which("sh")
        sh(
            "./configure",
            "--vars",
            "ASPELL={0}".format(aspell),
            "PREZIP={0}".format(prezip),
            "DESTDIR={0}".format(destdir),
        )


# Aspell dictionaries install their bits into their prefix.lib
# and when activated they'll get symlinked into the appropriate aspell's
# dict dir (see aspell's {de,}activate methods).
#
# They aren't really an Autotools package, but it's close enough
# that this works if we override configure().
class AspellDictPackage(AutotoolsPackage):
    """Specialized class for building aspell dictionairies."""

    spack.directives.extends("aspell", when="build_system=autotools")

    #: Override the default autotools builder
    AutotoolsBuilder = AspellBuilder

    def view_destination(self, view):
        aspell_spec = self.spec["aspell"]
        if view.get_projection_for_spec(aspell_spec) != aspell_spec.prefix:
            raise spack.package_base.ExtensionError(
                "aspell does not support non-global extensions"
            )
        aspell = aspell_spec.command
        return aspell("dump", "config", "dict-dir", output=str).strip()

    def view_source(self):
        return self.prefix.lib

    def patch(self):
        fs.filter_file(r"^dictdir=.*$", "dictdir=/lib", "configure")
        fs.filter_file(r"^datadir=.*$", "datadir=/lib", "configure")
