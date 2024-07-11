# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install linux
#
# You can edit this file again by typing:
#
#     spack edit linux
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Linux(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/torvalds/linux"
    url = "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.9.9.tar.xz"

    maintainers("fleshling", "rountree", "rountree-alt")

    license("GPL-2.0-only", checked_by="fleshling")

    version("6.9.9", sha256="2be05b487eb239a3bf687d628a8f104177d09c310f00bcc2a5e50f1733421eb9")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter("Makefile")
        # makefile.filter("CC = .*", "CC = cc")
        pass
