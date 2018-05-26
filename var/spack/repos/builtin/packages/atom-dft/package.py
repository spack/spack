##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
