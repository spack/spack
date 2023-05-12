# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Usalign(Package):
    """US-align (Universal Structural alignment) is a unified protocol
    to compare 3D structures of different macromolecules (proteins,
    RNAs and DNAs) in different forms (monomers, oligomers and
    heterocomplexes) for both pairwise and multiple structure
    alignments."""

    homepage = "https://zhanggroup.org/US-align"
    url = "https://zhanggroup.org/US-align/bin/module/USalign.cpp"

    maintainers("snehring")

    # date assumed from paper publication date
    version(
        "20220829",
        sha256="30274251f4123601af102cf6d4f1a9cc496878c1ae776702f554e2fc25658d7f",
        expand=False,
    )

    variant("fast-math", default=False)

    phases = ["build", "install"]

    def build(self, spec, prefix):
        cxx = Executable(self.compiler.cxx)
        args = ["-O3"]
        if spec.satisfies("+fast-math"):
            args.append("-ffast-math")
        args.extend(["-lm", "-o", "USalign", "USalign.cpp"])
        cxx(*args)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("USalign", prefix.bin)
