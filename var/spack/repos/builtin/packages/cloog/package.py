# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cloog(Package):
    """CLooG is a free software and library to generate code for
    scanning Z-polyhedra. That is, it finds a code (e.g. in C,
    FORTRAN...) that reaches each integral point of one or more
    parameterized polyhedra."""

    homepage = "http://www.cloog.org"
    url      = "http://www.bastoul.net/cloog/pages/download/count.php3?url=./cloog-0.18.1.tar.gz"
    list_url = "http://www.bastoul.net/cloog/pages/download"

    version('0.18.1', 'e34fca0540d840e5d0f6427e98c92252')
    version('0.18.0', 'be78a47bd82523250eb3e91646db5b3d')
    version('0.17.0', '0aa3302c81f65ca62c114e5264f8a802')

    depends_on("gmp")
    depends_on("isl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-osl=no",
                  "--with-isl=%s" % spec['isl'].prefix,
                  "--with-gmp=%s" % spec['gmp'].prefix)
        make()
        make("install")
