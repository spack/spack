# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AtomDft(MakefilePackage):
    """ATOM is a program for DFT calculations in atoms and pseudopotential
       generation."""

    homepage = "https://departments.icmab.es/leem/siesta/Pseudopotentials/"
    url      = "https://departments.icmab.es/leem/siesta/Pseudopotentials/Code/atom-4.2.6.tgz"

    version('4.2.6', 'c0c80cf349f951601942ed6c7cb0256b')

    depends_on('libgridxc')
    depends_on('xmlf90')

    def edit(self, spec, prefix):
        copy('arch.make.sample', 'arch.make')

    @property
    def build_targets(self):
        return ['XMLF90_ROOT=%s' % self.spec['xmlf90'].prefix,
                'GRIDXC_ROOT=%s' % self.spec['libgridxc'].prefix,
                'FC=fc']

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('atm', prefix.bin)
