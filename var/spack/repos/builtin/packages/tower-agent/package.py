# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class TowerAgent(Package):
    """Tower Agent allows Nextflow Tower to launch pipelines
    on HPC clusters that do not allow direct access through
    an SSH client.
    """

    homepage = "https://github.com/seqeralabs/tower-agent"

    if platform.machine() == "x86_64":
        if platform.system() == "Linux":
            version(
                "0.4.3",
                sha256="1125e64d4e3342e77fcf7f6827f045e421084654fe8faafd5389e356e0613cc0",
                url="https://github.com/seqeralabs/tower-agent/releases/download/v0.4.3/tw-agent-linux-x86_64",
                expand=False,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "tw-agent"))
        set_executable(join_path(prefix.bin, "tw-agent"))
