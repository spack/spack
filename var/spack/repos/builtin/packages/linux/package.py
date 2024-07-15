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
    """Linux is a clone of the operating system Unix and aims towards POSIX and 
    Single UNIX Specification compliance. It has all the features you would expect 
    in a modern fully-fledged Unix, including true multitasking, virtual memory, 
    shared libraries, demand loading, shared copy-on-write executables, proper memory 
    management, and multistack networking including IPv4 and IPv6."""

    homepage = "https://github.com/torvalds/linux"
    url = "https://github.com/fleshling/linux/archive/refs/heads/master.zip"

    maintainers("fleshling", "rountree", "rountree-alt")

    license("GPL-2.0-only", checked_by="fleshling")

    version("6.9.9", sha256="19e8dd54db1e338d59c17102d81edba7a988f9e1c7224c69165a9d442df8aac3")

    patch ("configured-linux.patch", when="@6.9.9:")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def edit(self, spec, prefix):
        # makefile = FileFilter("Makefile")
        # makefile.filter("CC = .*", "CC = cc")
        pass
