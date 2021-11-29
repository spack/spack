# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Roary(Package):
    """Rapid large-scale prokaryote pan genome analysis"""

    homepage = "https://github.com/sanger-pathogens/Roary"
    url      = "https://github.com/sanger-pathogens/Roary/archive/refs/tags/v3.13.0.tar.gz"

    maintainers = ['dorton21']

    version('3.13.0', sha256='375f83c8750b0f4dea5b676471e73e94f3710bc3a327ec88b59f25eae1c3a1e8')

    depends_on('parallel', type='run')
    depends_on('bedtools2', type='run')
    depends_on('cdhit', type='run')
    depends_on('prank', type='run')
    depends_on('blast-plus', type='run')
    depends_on('mcl', type='run')
    depends_on('fasttree', type='run')
    depends_on('mafft', type='run')
    depends_on('kraken', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', prefix.bin)
