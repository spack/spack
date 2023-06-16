# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Chexmix(Package):
    """ChExMix: the ChIP-exo mixture model. ChExMix aims to characterize protein-DNA binding
    subtypes in ChIP-exo experiments."""

    homepage = "http://mahonylab.org/software/chexmix"
    url = "https://github.com/seqcode/chexmix/releases/download/v0.52/chexmix.v0.52.public.jar"

    version(
        "0.52.public",
        sha256="7f856921b6071092cfcf226e4f99d9ab80587cf05502b41d00b8e5e16ccbfcdd",
        expand=False,
    )

    depends_on("java@8:", type="run")
    depends_on("meme", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "chexmix.v{0}.jar".format(self.version)
        install(jar_file, prefix.bin)

        # create a helper script to launch the .jar
        script_sh = join_path(os.path.dirname(__file__), "chexmix.sh")
        script = prefix.bin.chexmix
        install(script_sh, script)
        set_executable(script)
        # set the helper script to explicitly point to java and the .jar file
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("chexmix.jar", join_path(prefix.bin, jar_file), script, **kwargs)
