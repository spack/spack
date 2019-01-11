# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Porta(Package):
    """PORTA is a collection of routines for analyzing polytopes and
    polyhedra"""
    homepage = "http://porta.zib.de"
    url      = "http://porta.zib.de/porta-1.4.1.tgz"

    version('1.4.1', '585179bf19d214ed364663a5d17bd5fc')

    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def install(self, spec, prefix):
        with working_dir("src"):
            make("-f", "Makefile.spack", "PREFIX=%s" % prefix)
            make("-f", "Makefile.spack", "PREFIX=%s" % prefix, "install")
