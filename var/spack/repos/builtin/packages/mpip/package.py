# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Mpip(AutotoolsPackage):
    """mpiP: Lightweight, Scalable MPI Profiling"""
    homepage = "http://mpip.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/mpip/mpiP/mpiP-3.4.1/mpiP-3.4.1.tar.gz"

    version("3.4.1", "1168adc83777ac31d6ebd385823aabbd")

    depends_on("elf")
    depends_on("libdwarf")
    depends_on('libunwind', when=os.uname()[4] == "x86_64")
    depends_on("mpi")

    def configure_args(self):
        config_args = ['--without-f77']
        config_args.append("--with-cc=%s" % self.spec['mpi'].mpicc)
        config_args.append("--with-cxx=%s" % self.spec['mpi'].mpicxx)

        return config_args
