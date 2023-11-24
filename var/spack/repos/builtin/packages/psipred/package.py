# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Psipred(MakefilePackage):
    """PSIPRED (Position Specific Iterated Prediction) is a highly accurate
    method for protein secondary structure prediction."""

    homepage = "https://github.com/psipred/psipred"
    url = "https://github.com/psipred/psipred/archive/refs/tags/v4.0.tar.gz"

    version("4.0", sha256="ce4c901c8f152f6e93e4f70dc8079a5432fc64d02bcc0215893e33fbacb1fed2")

    depends_on("tcsh", type=("build", "run"))
    depends_on("blast-legacy@2.2.26", type="run")

    build_directory = "src"

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix)

    def install(self, spec, prefix):

        filter_file("set ncbidir = \/usr\/local\/bin", f"set ncbidir = {spec['blast-legacy'].prefix.bin}", "runpsipred")
        filter_file("#!\/bin\/tcsh", f"#!{spec['tcsh'].prefix.bin.tcsh}", "runpsipred")
        filter_file("#!\/bin\/tcsh", f"#!{spec['tcsh'].prefix.bin.tcsh}", "runpsipred_single")

        set_executable("runpsipred")
        set_executable("runpsipred_single")

        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)
        install("runpsipred*", prefix)
        mkdirp(prefix.join("BLAST+"))
        install_tree("BLAST+/", prefix.join("BLAST+"))
        mkdirp(prefix.data)
        install_tree("data/", prefix.data)
        mkdirp(prefix.example)
        install_tree("example/", prefix.example)
