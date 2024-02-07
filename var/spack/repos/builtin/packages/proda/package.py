# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Proda(MakefilePackage):
    """ProDA is public domain software for multiple alignment of protein sequences with
    repeated and shuffled elements"""

    homepage = "http://proda.stanford.edu/"
    url = "http://proda.stanford.edu/proda_1_0.tar.gz"

    version("1.0", sha256="439a93bf35e1a29ac1d5dde51e61f2cb174618596afaaaaa27d33a8ea1868a08")

    # update includes to bring inline with modern C++
    # (relevant patches taken from the bioconda recipe)
    patch("proda.patch")

    def url_for_version(self, version):
        return f"http://proda.stanford.edu/proda_{version.underscored}.tar.gz"

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CXX = .*", f"CXX = {spack_cxx}")
        makefile.filter(
            "CXXFLAGS = .*",
            "CXXFLAGS = -O3 -W -Wall -pedantic -DNDEBUG $(OTHERFLAGS) -funroll-loops",
        )

    def build(self, spec, prefix):
        make("proda")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("proda", prefix.bin)
