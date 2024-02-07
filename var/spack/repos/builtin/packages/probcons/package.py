# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Probcons(MakefilePackage):
    """PROBCONS is a novel tool for generating multiple alignments of protein sequences using
    a combination of probabilistic modeling and consistency-based alignment techniques"""

    homepage = "http://probcons.stanford.edu/about.html"
    url = "http://probcons.stanford.edu/probcons_v1_12.tar.gz"

    version("1.12", sha256="ecf3f9ab9ad47e14787c76d1c64aeea5533d4038c4be0236c00cdd79104cf383")

    # update includes to bring inline with modern C++
    # (from patch file in the bioconda recipe)
    patch("probcons.patch")

    def url_for_version(self, version):
        return f"http://probcons.stanford.edu/probcons_v{version.underscored}.tar.gz"

    def edit(self, spec, prefix):
        filter_file("CXX = .*", f"CXX = {spack_cxx}", "Makefile")

    def build(self, spec, prefix):
        make("probcons", "compare", "project")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for f in ("probcons", "compare", "project"):
            install(f, prefix.bin)
