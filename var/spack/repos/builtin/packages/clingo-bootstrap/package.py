# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkg.builtin.clingo import Clingo


class ClingoBootstrap(Clingo):
    """Clingo with some options used for bootstrapping"""
    variant('build_type', default='Release', values=('Release',),
            description='CMake build type')

    def setup_build_environment(self, env):
        env.set('CXXFLAGS', '-static-libstdc++ -static-libgcc -Wl,--exclude-libs,ALL')
        env.set('LDFLAGS', '-static-libstdc++ -static-libgcc -Wl,--exclude-libs,ALL')
