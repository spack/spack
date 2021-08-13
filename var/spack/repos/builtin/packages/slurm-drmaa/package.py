# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SlurmDrmaa(AutotoolsPackage):
    """Slurm-DRMAA is the Slurm implementation of DRMAA"""

    homepage = "https://github.com/natefoo/slurm-drmaa"
    url      = "https://github.com/natefoo/slurm-drmaa/releases/download/1.1.2/slurm-drmaa-1.1.2.tar.gz"

    version('1.2.0-dev.635b7ac', sha256='5aaf12e87010315ebf5217fe8a21003ab967c42b74efea33243dff221c85c2dc')

    depends_on("slurm")
    depends_on("gperf")

    def configure_args(self):
        args = []
        return args
