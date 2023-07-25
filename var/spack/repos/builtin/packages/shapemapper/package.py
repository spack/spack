# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shapemapper(CMakePackage):
    """
    ShapeMapper automates the calculation of RNA structure probing reactivities from mutational
    profiling (MaP) experiments, in which chemical adducts on RNA are detected as internal
    mutations in cDNA through reverse transcription and read out by massively parallel sequencing.
    """

    homepage = "https://github.com/Weeks-UNC/shapemapper2"
    url = "https://github.com/Weeks-UNC/shapemapper2/releases/download/2.1.5/shapemapper-2.1.5-source-only.tar.gz"

    maintainers("snehring")

    version(
        "2.1.5",
        sha256="0846a5d8b5f01d2d039fad4b957df0b6220a8505463f1a410368a1b90d2b227c",
        url="https://github.com/Weeks-UNC/shapemapper2/releases/download/2.1.5/shapemapper-2.1.5-source-only.tar.gz",
    )

    depends_on("bowtie2@2.3.0: ^perl+threads", type="run")
    # hard version dep due to jni
    depends_on("bbmap@37.78", type="run")
    depends_on("boost+filesystem+program_options+iostreams+system")
    depends_on("star@2.5.2:", type="run")
    depends_on("pv@1.6.0:", type="run")
    depends_on("python@3.7:", type="run")
    depends_on("graphviz@2.38.0:", type="run")
    depends_on("py-scikit-learn@0.18.1:", type="run")
    depends_on("py-matplotlib@1.5.1:3.3", type="run")

    build_directory = "build"

    def install(self, spec, prefix):
        for d in ["docs", "internals", "util"]:
            mkdirp(join_path(prefix, d))
            install_tree(d, join_path(prefix, d))
        for f in ["shapemapper", "README.md"]:
            install(f, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
