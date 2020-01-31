# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pythia8(AutotoolsPackage):
    """The Pythia program is a standard tool for the generation of events in
    high-energy collisions, comprising a coherent set of physics models for
    the evolution from a few-body hard process to a complex multiparticle
    final state."""

    homepage = "http://home.thep.lu.se/Pythia/"
    url      = "http://home.thep.lu.se/~torbjorn/pythia8/pythia8244.tgz"

    version('8301', sha256='51382768eb9aafb97870dca1909516422297b64ef6a6b94659259b3e4afa7f06')
    version('8244', sha256='e34880f999daf19cdd893a187123927ba77d1bf851e30f6ea9ec89591f4c92ca', preferred=True)

    variant('shared', default=True, description='Build shared library')

    def configure_args(self):
        args = []

        if '+shared' in self.spec:
            args.append('--enable-shared')

        return args
