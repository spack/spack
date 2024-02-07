# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tcoffee(MakefilePackage):
    """T-Coffee is a collection of tools for computing, evaluating and manipulating
    multiple alignments of DNA, RNA, protein sequences and structures"""

    homepage = "https://tcoffee.org/Projects/tcoffee/index.html"
    git = "https://github.com/cbcrg/tcoffee.git"
    url = "https://s3.eu-central-1.amazonaws.com/tcoffee-packages/Archives/T-COFFEE_distribution_Version_13.46.0.919e8c6b.tar.gz"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version(
        "13.46.0.919e8c6b",
        sha256="31fd0ca0734974c93cb68bef6e394f463a4589c3315fd28cf2bd41b8a167db22")
    version(
        "11.0",
        commit="f389b558e91d0f82e7db934d9a79ce285f853a71",
        deprecated=True,
    )

    depends_on("perl", type="run")
    depends_on("perl-soap-lite", type="run")
    depends_on("perl-xml-simple", type="run")

    # Dependencies taken from ./install script
    # TODO: lots of missing dependencies!
    # TODO: make variants for these as per the ./install script

    # depends_on("clustalo", type="run")
    # depends_on("strike", type="run")
    # depends_on("clustalw2", type="run")
    depends_on("clustalw", type="run")
    # depends_on("dialign-t", type="run")
    depends_on("dialign-tx", type="run")
    depends_on("poamsa", type="run")
    depends_on("probconsrna", type="run")
    # depends_on("msaprobs", type="run")
    # depends_on("upp", type="run")
    # depends_on("famsa", type="run")
    depends_on("mafft", type="run")
    # depends_on("msa", type="run")
    # depends_on("dca", type="run")
    depends_on("muscle", type="run")
    depends_on("pcma", type="run")
    # depends_on("kalign", type="run")
    # depends_on("amap", type="run")
    # depends_on("proda", type="run")
    # depends_on("prank", type="run")
    # depends_on("sap", type="run")
    depends_on("tmalign", type="run")
    # depends_on("mustang", type="run")
    # depends_on("fugue", type="run")
    # depends_on("dali-lite", type="run")
    # depends_on("sfold", type="run")
    depends_on("viennarna", type="run")
    # depends_on("retree", type="run")
    # depends_on("hmmtop", type="run")
    # depends_on("goriv", type="run")
    depends_on("blast-legacy", type="run")
    # depends_on("x3dna", type="run")
    # depends_on("fsa", type="run")

    @property
    def build_directory(self):
        if spec.satisfies("@13:"):
            return "t_coffee_source"
        else:
            return"compile"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("CC=g++", f"CC={spack_cxx}", "makefile")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("t_coffee")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("t_coffee", prefix.bin)
