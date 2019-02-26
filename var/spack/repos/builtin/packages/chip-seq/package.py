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


class ChipSeq(MakefilePackage):
    """The ChIP-Seq software provides methods for the analysis of ChIP-seq data
     and other types of mass genome annotation data."""

    homepage = "https://ccg.epfl.ch/chipseq"
    url      = "https://sourceforge.net/projects/chip-seq/files/chip-seq/1.5.5/chip-seq.1.5.5.tar.gz/download"

    version('1.5.5', '4e08c0558e2304415c766fa0bd3cbebd')
    version('1.5.4', 'faf1098bfd4e32a23c0a92309b81b2df')
    version('1.5.3', 'e60bc8392cb9ca9a661b3ea68f668184')

    depends_on('perl', type=('run',))

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        if '@:1.5.4' in self.spec:
            makefile.filter('binDir = .*', 'binDir = ' + self.prefix.bin)
            makefile.filter('mv', 'mkdir -p ${binDir}; mv')
        makefile.filter('CC = .*', 'CC = ' + env['CC'])

    @property
    def install_targets(self):
        targets = []
        if '@1.5.5:' in self.spec:
            targets = [
                'prefix={0}'.format(self.prefix), 'install-man', 'install-dat'
            ]

        targets += ['install']

        return targets
