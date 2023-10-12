# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fpocket
#
# You can edit this file again by typing:
#
#     spack edit fpocket
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Fpocket(MakefilePackage):
    """The fpocket suite of programs is a very fast open source protein pocket detection algorithm based on Voronoi tessellation."""

    homepage = "https://github.com/Discngine/fpocket"
    url = "https://github.com/Discngine/fpocket/archive/refs/tags/4.1.tar.gz"

    version('4.1', '1a2af2d3f2df42de67301996db3b93c7eaff0375f866443c0468dcf4b1750688', extension='tar.gz')

    depends_on("netcdf-c")
    depends_on("netcdf-cxx")

    def setup_build_environment(self, env):
        if self.compiler.name == "gcc":
            env.set("CXX", "g++")

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("BINDIR .*", "BINDIR = %s/bin" % prefix)
        makefile.filter("MANDIR .*", "MANDIR = %s/man/man8" % prefix)

    def install(self, spec, prefix):
        make()
        make("install")
