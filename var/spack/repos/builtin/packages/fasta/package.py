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


class Fasta(MakefilePackage):
    """The FASTA programs find regions of local or global similarity
    between Protein or DNA sequences, either by searching Protein or
    DNA databases, or by identifying local duplications within a
    sequence. Other programs provide information on the statistical
    significance of an alignment. Like BLAST, FASTA can be used to
    infer functional and evolutionary relationships between sequences
    as well as help identify members of gene families.
    """

    homepage = "https://fasta.bioch.virginia.edu/fasta_www2/fasta_list2.shtml"
    url      = "https://github.com/wrpearson/fasta36/archive/fasta-v36.3.8g.tar.gz"

    version('36.3.8g', sha256='fa5318b6f8d6a3cfdef0d29de530eb005bfd3ca05835faa6ad63663f8dce7b2e')

    depends_on('zlib')

    # The src tree includes a plethora of variant Makefiles and the
    # builder is expected to choose one that's appropriate.  This'll
    # do for a first cut.  I can't test anything else....
    @property
    def makefile_name(self):
        if self.spec.satisfies('platform=darwin'):
            name = 'Makefile.os_x86_64'
        elif (self.spec.satisfies('platform=linux') and
              self.spec.satisfies('target=x86_64')):
            name = 'Makefile.linux64_sse2'
        else:
            tty.die('''Unsupported platform/target, must be
Darwin (assumes 64-bit)
Linux x86_64
''')
        return name

    @property
    def makefile_path(self):
        return join_path(self.stage.source_path, 'make', self.makefile_name)

    def edit(self, spec, prefix):
        makefile = FileFilter(self.makefile_path)
        makefile.filter('XDIR = .*', 'XDIR = {0}'.format(prefix.bin))

    def build(self, spec, prefix):
        with working_dir('src'):
            make('-f', self.makefile_path)

    def install(self, spec, prefix):
        with working_dir('src'):
            mkdir(prefix.bin)
            make('-f', self.makefile_path, 'install')
