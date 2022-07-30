# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class TowerCli(Package):
    """Tower on the Command Line brings Nextflow Tower concepts
    including Pipelines, Actions and Compute Environments
    to the terminal.
    """

    homepage = "https://github.com/seqeralabs/tower-cli"

    if platform.machine() == "x86_64":
        if platform.system() == "Darwin":
            version(
                "0.6.2",
                sha256="2bcc17687d58d4c888e8d57b7f2f769a2940afb3266dc3c6c48b0af0cb490d91",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.2/tw-0.6.2-osx-x86_64",
                expand=False,
            )
        elif platform.system() == "Linux":
            version(
                "0.6.2",
                sha256="02c6d141416b046b6e8b6f9723331fe0e39d37faa3561c47c152df4d33b37e50",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.2/tw-0.6.2-linux-x86_64",
                expand=False,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "tw"))
        set_executable(join_path(prefix.bin, "tw"))
