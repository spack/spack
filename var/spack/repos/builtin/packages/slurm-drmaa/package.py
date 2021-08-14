# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SlurmDrmaa(AutotoolsPackage):
    '''
    DRMAA for Slurm is an implementation of Open Grid Forum DRMAA 1.0 (Distributed
    Resource Management Application API) specification for submission and control of
    jobs to SLURM.  Using DRMAA, grid applications builders, portal developers and
    ISVs can use the same high-level API to link their software with different
    cluster/resource management systems.
    '''
    homepage = "https://github.com/natefoo/slurm-drmaa"
    url      = "https://github.com/natefoo/slurm-drmaa/releases/download/1.1.2/slurm-drmaa-1.1.2.tar.gz"

    maintainers = ['pwablito']

    version('1.2.0-dev.635b7ac', sha256='5aaf12e87010315ebf5217fe8a21003ab967c42b74efea33243dff221c85c2dc')

    depends_on("slurm")
    depends_on("gperf")
    depends_on("ragel")

    def configure_args(self):
        args = []
        return args
