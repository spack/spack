# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(MakefilePackage):
    """Lightweight user-defined software stacks for HPC."""

    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.9.9/charliecloud-0.9.9.tar.gz"

    version('0.9.10', sha256='44e821b62f9c447749d3ed0d2b2e44d374153058814704a5543e83f42db2a45a')
    version('0.9.9',  sha256='2624c5a0b19a01c9bca0acf873ceeaec401b9185a23e9108fadbcee0b9d74736')

    @property
    def install_targets(self):
        return ['install', 'PREFIX=%s' % self.prefix]
