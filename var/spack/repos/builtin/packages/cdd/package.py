# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cdd(Package):
    """The program cdd+ (cdd, respectively) is a C++ (ANSI C)
    implementation of the Double Description Method [MRTT53] for
    generating all vertices (i.e. extreme points) and extreme rays of
    a general convex polyhedron given by a system of linear
    inequalities"""
    homepage = "https://www.inf.ethz.ch/personal/fukudak/cdd_home/cdd.html"
    url      = "http://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-061a.tar.gz"

    version('0.61a', '22c24a7a9349dd7ec0e24531925a02d9')

    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def url_for_version(self, version):
        url = "http://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack", "PREFIX=%s" % prefix]
        make(*makeargs)
        make("install", *makeargs)
