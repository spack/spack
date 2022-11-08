# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install ycruncher
#
# You can edit this file again by typing:
#
#     spack edit ycruncher
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Ycruncher(Package):
    """
    y-cruncher is a program that can compute Pi and other constants to
    trillions of digits. It is the first of its kind that is multi-threaded
    and scalable to multi-core systems
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.numberworld.org/y-cruncher/"
    url = "http://www.numberworld.org/y-cruncher/y-cruncher%20v0.7.10.9513-static.tar.xz"
    maintainers = ["saqibkh"]

    version("0.7.10.9513", "292006496bba83bf0f8c354ceb1c2ea571f0c67b9fe46297701a8d387773db1b")

    depends_on("autoconf")

    def install(self, spec, prefix):
        install_tree(".", prefix)
