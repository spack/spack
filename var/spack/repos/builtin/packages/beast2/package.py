# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Beast2(Package):
    """BEAST is a cross-platform program for Bayesian inference using MCMC
       of molecular sequences. It is entirely orientated towards rooted,
       time-measured phylogenies inferred using strict or relaxed molecular
       clock models. It can be used as a method of reconstructing phylogenies
       but is also a framework for testing evolutionary hypotheses without
       conditioning on a single tree topology."""

    homepage = "http://beast2.org/"
    url      = "https://github.com/CompEvol/beast2/releases/download/v2.4.6/BEAST.v2.4.6.Linux.tgz"

    version('2.6.3', sha256='8899277b0d7124ab04dc512444d45f0f1a13505f3ce641e1f117098be3e2e20d')
    version('2.6.2', sha256='9b6882e7f825e16a4dd91548e43b71b10931a8b0c128a1c6ae90a185c7c6dca3')
    version('2.6.0', sha256='b7ae682904cec3a0c33f7d8b2f9d840afe5c00a3f0db6bd7aade7cfd7629dd76')
    version('2.5.2', sha256='2feb2281b4f7cf8f7de1a62de50f52a8678ed0767fc72f2322e77dde9b8cd45f')
    version('2.4.6', sha256='84029c5680cc22f95bef644824130090f5f12d3d7f48d45cb4efc8e1d6b75e93')

    depends_on('java')

    def setup_run_environment(self, env):
        env.set('BEAST', self.prefix)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('examples', join_path(self.prefix, 'examples'))
        install_tree('images', join_path(self.prefix, 'images'))
        install_tree('lib', prefix.lib)
        install_tree('templates', join_path(self.prefix, 'templates'))
