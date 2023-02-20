# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
    maintainers("marcodelapierre")

    if platform.machine() == "x86_64":
        if platform.system() == "Linux":
            version(
                "0.4.5",
                sha256="d3f38931ff769299b9f9f7e78d9f6a55f93914878c09117b8eaf5decd0c734ec",
                deprecated=True,
                url="https://github.com/seqeralabs/tower-agent/releases/download/v0.4.5/tw-agent-linux-x86_64",
                expand=False,
            )
            version(
                "0.4.3",
                sha256="1125e64d4e3342e77fcf7f6827f045e421084654fe8faafd5389e356e0613cc0",
                deprecated=True,
                url="https://github.com/seqeralabs/tower-agent/releases/download/v0.4.3/tw-agent-linux-x86_64",
                expand=False,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "tw-agent"))
        set_executable(join_path(prefix.bin, "tw-agent"))
