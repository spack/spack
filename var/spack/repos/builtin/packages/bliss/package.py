# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Bliss(Package):
    """bliss: A Tool for Computing Automorphism Groups and Canonical
    Labelings of Graphs"""

    homepage = "http://www.tcs.hut.fi/Software/bliss/"
    url = "http://www.tcs.hut.fi/Software/bliss/bliss-0.73.zip"

    version('0.73', '72f2e310786923b5c398ba0fc40b42ce')

    # Note: Bliss can also be built without gmp, but we don't support this yet

    depends_on("gmp")
    depends_on("libtool", type='build')

    patch("Makefile.spack.patch")

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack",
                    "PREFIX=%s" % prefix, "GMP_PREFIX=%s" % spec["gmp"].prefix]
        make(*makeargs)
        make("install", *makeargs)
