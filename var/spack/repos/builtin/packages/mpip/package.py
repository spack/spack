# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Mpip(AutotoolsPackage):
    """mpiP: Lightweight, Scalable MPI Profiling"""
    homepage = "http://mpip.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/mpip/mpiP/mpiP-3.4.1/mpiP-3.4.1.tar.gz"
    git      = "https://github.com/llnl/mpip.git"

    version('master', branch='master')
    version("3.4.1", sha256="688bf37d73211e6a915f9fc59c358282a266d166c0a10af07a38a01a473296f0")

    variant('shared', default=False, description="Build the shared library")
    variant('demangling', default=False, description="Build with demangling support")
    variant('setjmp',
            default=False,
            description="Replace glic backtrace() with setjmp for stack trace")

    depends_on("elf")
    depends_on("libdwarf")
    depends_on('libunwind', when=os.uname()[4] == "x86_64")
    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []
        if '+shared' in self.spec:
            targets.append('shared')

        return targets

    def configure_args(self):
        config_args = ['--without-f77']
        config_args.append("--with-cc=%s" % self.spec['mpi'].mpicc)
        config_args.append("--with-cxx=%s" % self.spec['mpi'].mpicxx)

        if '+demangling' in self.spec:
            config_args.append('--enable-demangling')
        else:
            config_args.append('--disable-demangling')

        if '+setjmp' in self.spec:
            config_args.append('--enable-setjmp')
        else:
            config_args.append('--disable-setjmp')

        return config_args
