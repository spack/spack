# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Quicksilver(MakefilePackage):
    """Quicksilver is a proxy application that represents some elements of
    the Mercury workload by solving a simpli?ed dynamic monte carlo
    particle transport problem.  Quicksilver attempts to replicate the
    memory access patterns, communication patterns, and the branching or
    divergence of Mercury for problems using multigroup cross sections."""

    homepage = "https://codesign.llnl.gov/quicksilver.php"
    git      = "https://github.com/LLNL/Quicksilver.git"

    version('master', branch='master')

    def build(self, spec, prefix):
        with working_dir('src'):
            arg = 'CXX={0}'.format(spack_cxx)
            make(arg)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('./src/qs', prefix.bin)
        install_tree('Examples', prefix.Examples)
