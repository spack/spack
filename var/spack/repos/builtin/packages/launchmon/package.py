# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Launchmon(Package):
    """Software infrastructure that enables HPC run-time tools to
       co-locate tool daemons with a parallel job."""
    homepage = "https://github.com/LLNL/LaunchMON"
    url = "https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz"

    version('1.0.2', '8d6ba77a0ec2eff2fde2c5cc8fa7ff7a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('libgcrypt')
    depends_on('libgpg-error')
    depends_on("elf", type='link')
    depends_on("boost")
    depends_on("spectrum-mpi", when='arch=ppc64le')

    def install(self, spec, prefix):
        configure(
            "--prefix=" + prefix,
            "--with-bootfabric=cobo",
            "--with-rm=slurm")

        make()
        make("install")
