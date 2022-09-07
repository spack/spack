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
#     spack install starship
#
# You can edit this file again by typing:
#
#     spack edit starship
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Starship(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://starship.rs"
    url = "https://github.com/starship/starship/releases/download/v1.10.2/starship-x86_64-unknown-linux-gnu.tar.gz"
    maintainers = [
        "andrewda",
        "andytom",
        "ATiltedTree",
        "cappyzawa",
        "davidkna",
        "heyrict",
        "jimleroyer",
        "jletey",
        "kidonng",
        "matchai",
        "Snuggle",
        "tiffafoo",
        "vladimyr",
        "wyze",
    ]

    version("1.10.2", sha256="253a62e48c1b15d5465c876560b71e1d3485697e22ab7adea85e37cbe1a70a54")


    def install(self, spec, prefix):
        make()
        make("install")
