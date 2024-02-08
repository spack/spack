# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

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
    depends_on("perl-xml-simple", type="run")

    # t_coffee / common dependencies
    depends_on("strike", type="run")
    depends_on("gor", type="run")
    depends_on("blast-plus", type="run")
    depends_on("mafft", type="run")
    depends_on("clustal-omega", type="run")

    #
    # Variants and their required dependencies are taken from the ./install script (L1642-)
    #
    # Notes:
    # - `x3dna`, `hmmtop`, and `fugue` are distributed manually / under manual license
    #   agreement. These have been removed to allow simpler install of the package.
    # - `saracoffee` variant is disabled for now due to dependency on `x3dna`.
    # - `dialign-tx` doesn't compile properly and is remaining as an optional dependency
    # - `lsqman` and `align_pdb` are extremely old. I can't find a extant source of these
    #   programs and/or can't persuade them to compile.
    #

    variant("mcoffee", default=False, description="Meta-alignment with multiple MSA programs")
    variant("psicoffee", default=False, description="Homology extended MSA")
    variant("expresso", default=False, description="Very accurate structure-based MSA")
    variant("3dcoffee", default=False, description="Multiple structure alignments")
    variant("rcoffee", default=False, description="RNA MSA")
    # variant("saracoffee", default=False, description="Structure-based multiple RNA alignment")
    variant("trmsd", default=False, description="RMSD-based structural clustering of related proteins")

    with when("+mcoffee"):
        depends_on("clustalw", type="run") # this is clustalw2
        depends_on("dialign", type="run") # this is dialign-t
        # depends_on("dialign-tx", type="run")
        depends_on("poamsa", type="run")
        depends_on("probcons", type="run")
        depends_on("probconsrna", type="run")
        depends_on("msaprobs", type="run")
        depends_on("famsa", type="run")
        depends_on("msa", type="run")
        depends_on("dca", type="run")
        depends_on("muscle", type="run")
        depends_on("pcma", type="run")
        depends_on("kalign", type="run")
        depends_on("amap", type="run")
        depends_on("proda", type="run")
        depends_on("prank", type="run")
        depends_on("fsa", type="run")

    with when("+expresso") or when("+3dcoffee"):
        depends_on("sap", type="run")
        depends_on("tmalign", type="run")
        depends_on("mustang", type="run")
        # depends_on("lsqman", type="run")
        # depends_on("pdb_align", type="run")
        # depends_on("fugue", type="run")

    with when("+psicoffee"):
        # depends_on("hmmtop", type="run")
        pass

    with when("+rcoffee"):
        depends_on("clustalw", type="run") # this is clustalw2
        depends_on("famsa", type="run")
        depends_on("muscle", type="run")
        depends_on("probconsrna", type="run")
        depends_on("consan", type="run")
        depends_on("viennarna", type="run")

    # with when("+saracoffee"):
    #     depends_on("x3dna", type="run")

    with when("+trmsd"):
        depends_on("phylip", type="run")

    @property
    def build_directory(self):
        if self.spec.satisfies("@13:"):
            return "t_coffee_source"
        else:
            return "compile"

    @property
    def sys_max_pid(self):
        if self.spec.satisfies("platform=darwin"):
            return 99998
        try:
            with open("/proc/sys/kernel/pid_max") as f:
                return f.read().strip()
        except:
            return 4194304 # 64-bit default

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("CC=.*", f"CC={spack_cxx}", "makefile")
            filter_file("#define MAX_N_PID.*", f"#define MAX_N_PID {self.sys_max_pid}", "coffee_defines.h")

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            flags.append("-std=c++11")
        return flags, None, None

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("t_coffee")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("t_coffee", prefix.bin)
        install_tree("mcoffee", prefix.mcoffee)

    def setup_run_environment(self, env):
        env.set("MCOFFEE_4_TCOFFEE", self.prefix.mcoffee)
