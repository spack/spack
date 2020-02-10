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
    version('8240', sha256='d27495d8ca7707d846f8c026ab695123c7c78c7860f04e2c002e483080418d8d')
    version('8235', sha256='e82f0d6165a8250a92e6aa62fb53201044d8d853add2fdad6d3719b28f7e8e9d')
    version('8230', sha256='332fad0ed4f12e6e0cb5755df0ae175329bc16bfaa2ae472d00994ecc99cd78d')
    version('8212', sha256='f8fb4341c7e8a8be3347eb26b00329a388ccf925313cfbdba655a08d7fd5a70e')

    variant('shared', default=True, description='Build shared library')

    depends_on('rsync', type='build')

    def configure_args(self):
        args = []

        if '+shared' in self.spec:
            args.append('--enable-shared')

        return args
