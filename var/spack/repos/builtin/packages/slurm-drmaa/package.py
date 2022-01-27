# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    git      = 'https://github.com/natefoo/slurm-drmaa.git'

    maintainers = ['pwablito']

    version('main', branch='main',  submodules=True)
    version('1.1.2', sha256='5bfe25d501de83729df3c8c8f28535b9da3e99aea7738e259903abd6f1f5c836')

    # Remove this patch when it is merged into main:
    patch('https://patch-diff.githubusercontent.com/raw/natefoo/slurm-drmaa/pull/62.patch',
          sha256='86bba5e2683f33e59f7e9193aa5fa948eb6a5507d44768f2f6d756a33fef7b74',
          when='@main')

    depends_on('autoconf', type='build', when='@main')
    depends_on('automake', type='build', when='@main')
    depends_on('libtool',  type='build', when='@main')
    depends_on('bison',    type='build', when='@main')

    depends_on("slurm")
    depends_on("slurm@:20-11-8-1", when='@1.1.2')
    depends_on("gperf")
    depends_on("ragel")

    def check(self):
        pass
