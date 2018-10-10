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
import os


class Treesub(Package):
    """A small program (which glues together other programs) that
       allows a user to input a codon alignment in FASTA format and
       produce an annotated phylogenetic tree showing which substitutions
       occurred on a given branch. Originally written for colleagues at
       the MRC NIMR."""

    homepage = "https:/github.com/tamuri/treesub"
    url      = "https://github.com/tamuri/treesub/archive/v0.2.tar.gz"

    version('0.2', sha256='58b0d2638cf9ae1ad8705df26a57c32b52a69f50e7954debbd678c82772fdc56')
    version('0.1', sha256='c083ecc5f7e9f11645a7e768f6a09fefcbb254b526212003527b4b8dd14723f1')

    depends_on('jdk', type='run')
    depends_on('ant', type='build')
    depends_on('paml', type='run')
    depends_on('raxml', type='run')
    depends_on('figtree', type='run')

    def install(self, spec, prefix):
        ant = self.spec['ant'].command
        ant('jar')

        mkdirp(prefix.bin)
        install_tree('dist', prefix.bin)

        mkdirp(prefix.lib)
        install_tree('lib', prefix.lib)

        execscript = join_path(self.package_dir, 'treesub')
        os.chmod(execscript, 0o775)
        install(execscript, prefix.bin)
