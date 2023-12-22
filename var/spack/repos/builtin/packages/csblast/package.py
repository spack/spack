# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Csblast(MakefilePackage):
    """Context-Specific BLAST is a tool that searches a protein sequence
    that extends BLAST (Basic Local Alignment Search Tool)
    using context-specific mutation probabilities
    """

    homepage = "https://github.com/cangermueller/csblast"
    url = "https://github.com/cangermueller/csblast/archive/refs/tags/v2.2.3.tar.gz"

    version("2.2.4", sha256="76848da4d45a618ae903cafc00ff6387e7decb17b839aca83d9a9438537edf0d")
    version("2.2.3", sha256="3cf8dc251e85af6942552eae3d33e45a5a1c6d73c5e7f1a00ce26d6974c0d434")

    depends_on("sparsehash", type=("build", "run"))

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["sparsehash"].prefix.include)

    def build(self, spec, prefix):
        with working_dir(join_path(self.stage.source_path, "src")):
            filter_file(
                r"INC = -I\$\$HOME\/include",
                f"INC = -I{self.spec['sparsehash'].prefix.include}",
                "Makefile",
            )
            make("csblast")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)
