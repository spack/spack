# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dca(MakefilePackage):
    """Divide-and-Conquer Multiple Sequence Alignment ( DCA) is a program for producing
    fast, high quality simultaneous multiple sequence alignments of amino acid, RNA, or
    DNA sequences"""

    homepage = "https://bibiserv.cebitec.uni-bielefeld.de/dca"
    url = "https://bibiserv.cebitec.uni-bielefeld.de/applications/dca/resources/downloads/dca-1.1-src.tar.gz"

    version("1.1", sha256="b90ab90e18503a62b03ceab96747d9150f03600ef4ad547a5bb5a15030a250db")

    depends_on("msa@2.1", type="run")

    def edit(self, spec, prefix):
        filter_file("CC = .*", f"CC = {spack_cc}", "Makefile")

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("bin", "dca"), prefix.bin)
        install_tree("cost", prefix.cost)

    def setup_run_environment(self, env):
        env.set("DCA_COST_DIR", self.prefix.cost)
