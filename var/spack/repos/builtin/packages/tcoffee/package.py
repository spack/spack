# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tcoffee(MakefilePackage):
    """T-Coffee is a collection of tools for computing, evaluating and manipulating
    multiple alignments of DNA, RNA, protein sequences and structures"""

    homepage = "https://tcoffee.org/Projects/tcoffee/index.html"

    # tcoffee is officially distributed through
    #   https://tcoffee.org/Projects/tcoffee/index.html
    # however these source bundles do not build properly with spack - error-free completion
    # but the binary segfaults. These bundles are generated from a CI pipeline running on
    # the top-level GitHub source, which does build properly, so we use that...
    git = "https://github.com/cbcrg/tcoffee.git"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version("13.46.0.919e8c6b", tag="Version_13.46.0.919e8c6b")
    version("11.0", commit="f389b558e91d0f82e7db934d9a79ce285f853a71", deprecated=True)

    depends_on("perl", type=("build", "link", "run"))
    depends_on("perl-xml-simple", type="run")
    depends_on("perl-soap-lite", type="run")

    # t_coffee / common dependencies
    depends_on("strike", type="run")
    depends_on("gor", type="run")
    depends_on("blast-plus", type="run")
    depends_on("mafft", type="run")
    depends_on("clustal-omega", type="run")

    # Variants and their required dependencies are formed by parsing the program:mode pairs
    # within the ./lib/data_headers/tclinkdb.txt file.
    #
    # Notes on listed dependencies:
    # * All dependencies are technically optional. They extend the core functionality.
    # - `x3dna`, `hmmtop`, and `fugue` are distributed manually / under manual license
    #   agreement. These have been removed here to allow simpler install of the package.
    #   - `saracoffee` variant is a stub due to dependency on `x3dna`.
    # - `lsqman` and `align_pdb` are extremely old. I can't find extant / reputable sources
    #   for these programs.
    # - `dialign-t` has disappeared in favour of its successor `dialign-tx`. I can't find an
    #   extant download for this version.
    # - `muscle4` was never released properly and is dropped here. This was an experimental
    #   version between `3` and `muscle5`.
    # - The version of `upp` expected by tcoffee is obsolete and the dependency is dropped
    #   here. UPP2 is now distributed with `sepp` but has a different interface.

    variant("all", default=True, description="Enable all functionality", sticky=True)
    variant("mcoffee", default=False, description="Meta-alignment with multiple MSA programs")
    variant("psicoffee", default=False, description="Homology extended MSA")
    variant("expresso", default=False, description="Very accurate structure-based MSA")
    variant("3dcoffee", default=False, description="Multiple structure alignments")
    variant("rcoffee", default=False, description="RNA MSA")
    # variant("saracoffee", default=False, description="Structure-based multiple RNA alignment")
    variant("trmsd", default=False, description="RMSD-based structural clustering of proteins")
    variant(
        "seq_reformat", default=False, description="Clean, reformat, and compare MSAs and trees"
    )

    # ensure ~all is explicit when +variants are declared
    for v in ("mcoffee", "psicoffee", "expresso", "3dcoffee", "rcoffee", "trmsd", "seq_reformat"):
        conflicts(f"+{v}", when="+all")

    with when("+all") or when("+mcoffee"):
        depends_on("clustalw", type="run")  # this is clustalw2
        depends_on("dialign-tx", type="run")
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

    with when("+all") or when("+expresso") or when("+3dcoffee"):
        depends_on("sap", type="run")
        depends_on("tmalign", type="run")
        depends_on("mustang", type="run")
        # depends_on("lsqman", type="run")
        # depends_on("pdb_align", type="run")
        # depends_on("fugue", type="run")

    with when("+all") or when("+psicoffee"):
        # depends_on("hmmtop", type="run")
        pass

    with when("+all") or when("+rcoffee"):
        depends_on("clustalw", type="run")  # this is clustalw2
        depends_on("famsa", type="run")
        depends_on("muscle", type="run")
        depends_on("probconsrna", type="run")
        depends_on("consan", type="run")
        depends_on("viennarna", type="run")

    with when("+all") or when("+trmsd"):
        depends_on("phylip", type="run")

    with when("+all") or when("+seq_reformat"):
        depends_on("phylip", type="run")
        depends_on("viennarna", type="run")

    build_directory = "t_coffee/src"

    parallel = False

    @property
    def sys_max_pid(self):
        if self.spec.satisfies("platform=darwin"):
            return 99998
        try:
            with open("/proc/sys/kernel/pid_max") as f:
                return f.read().strip()
        except (FileNotFoundError, IOError):
            return 4194304  # 64-bit default

    def edit(self, spec, prefix):
        filter_file("CC =.*", f"CC = {spack_cxx}", join_path(self.build_directory, "makefile"))
        filter_file(
            "#define MAX_N_PID.*",
            f"#define MAX_N_PID {self.sys_max_pid}",
            join_path("lib", "coffee_defines.h"),
        )

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("t_coffee")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "t_coffee"), prefix.bin)
        install_tree(join_path("lib", "mcoffee"), prefix.mcoffee)

    def setup_run_environment(self, env):
        env.set("MCOFFEE_4_TCOFFEE", self.prefix.mcoffee)
