# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Evtgen(AutotoolsPackage):
    """ EvtGen is a Monte Carlo event generator that simulates
        the decays of heavy flavour particles, primarily B and D mesons. """

    homepage = "https://evtgen.hepforge.org/"
    url      = "https://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/evtgen-1.7.0.tar.gz"

    maintainers = ['vvolkl']

    version('1.7.0', sha256='ec5c680f14b301888d6e265ef421e3fd36826cd7c9d8598f12aeb748ed8a2363')

    variant('pythia8', default=True, description='Build with pythia8')
    variant('tauola', default=False, description='Build with tauola')
    variant('photos', default=False, description='Build with photos')

    patch("g2c.patch")

    depends_on('hepmc@:2.99.99')
    depends_on("pythia8", when="+pythia8")
    depends_on("tauola", when="+tauola")
    depends_on("photos", when="+photos")

    def configure_args(self):
        args = []

        args.append('--hepmcdir=%s' % self.spec["hepmc"].prefix)
        if '+pythia8' in self.spec:
            args.append('--pythiadir=%s' % self.spec['pythia8'].prefix)
        if '+photos' in self.spec:
            args.append('--photosdir=%s' % self.spec['photos'].prefix)
        if '+tauola' in self.spec:
            args.append('--tauoladir=%s' % self.spec['tauola'].prefix)

        return args

    def build(self, spec, prefix):
        # avoid parallel compilation errors
        # due to libext_shared depending on lib_shared
        make('lib_shared')
        make('all')
