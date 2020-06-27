# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import glob
from spack import *


class Gatk(Package):
    """
    Genome Analysis Toolkit
    Variant Discovery in High-Throughput Sequencing Data
    """

    homepage = "https://software.broadinstitute.org/gatk/"
    url = "https://github.com/broadinstitute/gatk/releases/download/4.1.0.0/gatk-4.1.0.0.zip"
    list_url = "https://github.com/broadinstitute/gatk/releases"

    version(
        "4.1.0.0",
        sha256="148aa061328d922a570d0120d88f27e61e5da877f542206f4d77f2d788b7d21d",
    )
    version(
        "4.0.12.0",
        sha256="733134303f4961dec589247ff006612b7a94171fab8913c5d44c836aa086865f",
    )
    version(
        "4.0.11.0",
        sha256="5ee23159be7c65051335ac155444c6a49c4d8e3515d4227646c0686819934536",
    )
    version(
        "4.0.8.1",
        sha256="e4bb082d8c8826d4f8bc8c2f83811d0e81e5088b99099d3396d284f82fbf28c9",
    )
    version(
        "4.0.4.0",
        sha256="801bbb181c275cfabc96dc0cb21f3f901634cec11efde9ba9c8b91e2834feef4",
    )
    version(
        "3.8-1",
        sha256="a0829534d2d0ca3ebfbd3b524a9b50427ff238e0db400d6e9e479242d98cbe5c",
        extension="tar.bz2",
        url="https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.8-1-0-gf15c1c3ef",
    )
    version(
        "3.8-0",
        sha256="d1017b851f0cc6442b75ac88dd438e58203fa3ef1d1c38eb280071ae3803b9f1",
        extension="tar.gz",
        url="https://software.broadinstitute.org/gatk/download/auth?package=GATK",
    )

    depends_on("java@8", type="run")
    depends_on("python@2.6:2.8,3.6:", type="run", when="@4.0:")
    depends_on("r@3.2:", type="run", when="@4.0:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        # For ver 3.x will install "GenomeAnalysisTK.jar"
        # For ver 4.x will install both "gatk-package-<ver>-local.jar"
        # and "gatk-package-<ver>-spark.jar"
        for file in glob.glob("*.jar"):
            install(file, prefix.bin)

        # Skip helper script for versions >4.0
        if spec.satisfies("@4.0:"):
            install("gatk", prefix.bin)
        else:
            # Set up a helper script to call java on the jar file,
            # explicitly codes the path for java and the jar file.
            script_sh = join_path(os.path.dirname(__file__), "gatk.sh")
            script = join_path(prefix.bin, "gatk")
            install(script_sh, script)
            set_executable(script)

            # Munge the helper script to explicitly point to java and the
            # jar file.
            java = join_path(self.spec["java"].prefix, "bin", "java")
            kwargs = {"ignore_absent": False, "backup": False, "string": False}
            filter_file("^java", java, script, **kwargs)
            filter_file(
                "GenomeAnalysisTK.jar",
                join_path(prefix.bin, "GenomeAnalysisTK.jar"),
                script,
                **kwargs
            )

    def setup_run_environment(self, env):
        env.prepend_path(
            "GATK", join_path(self.prefix.bin, "GenomeAnalysisTK.jar")
        )
