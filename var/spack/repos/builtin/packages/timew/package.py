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
#     spack install timew
#
# You can edit this file again by typing:
#
#     spack edit timew
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Timew(CMakePackage):
    """
    Timewarrior is Free and Open Source Software that tracks time from the
    command line.
    """

    homepage = "https://timewarrior.net/"
    url = "https://github.com/GothenburgBitFactory/timewarrior/releases/download/v1.7.1/timew-1.7.1.tar.gz"

    license("MIT", checked_by="taliaferro")

    version("1.7.1", sha256="5e0817fbf092beff12598537c894ec1f34b0a21019f5a3001fe4e6d15c11bd94")

    # depends_on("foo")
