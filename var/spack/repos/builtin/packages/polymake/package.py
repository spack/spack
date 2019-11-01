# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Polymake(Package):
    """polymake is open source software for research in polyhedral geometry"""
    homepage = "https://polymake.org/doku.php"
    url      = "https://polymake.org/lib/exe/fetch.php/download/polymake-3.0r1.tar.bz2"

    version('3.0r2', sha256='e7c0f8e3a45ea288d2fb4ae781a1dcea913ef9c275fed401632cdb11a672d6dc')
    version('3.0r1', sha256='cdc223716b1cc3f4f3cc126089a438f9d12390caeed78291a87565717c7b504d')

    # Note: Could also be built with nauty instead of bliss

    depends_on("bliss")
    depends_on("boost")
    depends_on("cddlib")
    depends_on("gmp")
    depends_on("lrslib")
    depends_on("mpfr")
    depends_on("ppl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-bliss=%s" % spec["bliss"].prefix,
                  "--with-boost=%s" % spec["boost"].prefix,
                  "--with-cdd=%s" % spec["cddlib"].prefix,
                  "--with-gmp=%s" % spec["gmp"].prefix,
                  "--with-lrs=%s" % spec["lrslib"].prefix,
                  "--with-mpfr=%s" % spec["mpfr"].prefix,
                  "--with-ppl=%s" % spec["ppl"].prefix)
        make()
        make("install")
