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


class Orthofinder(Package):
    """OrthoFinder is a fast, accurate and comprehensive analysis tool for
    comparative genomics.

    It finds orthologues and orthogroups infers rooted  gene trees for all
    orthogroups and infers a rooted species tree for the species being
    analysed. OrthoFinder also provides comprehensive statistics for
    comparative genomic analyses. OrthoFinder is simple to use and all you
    need to run it is a set of protein sequence files (one per species)
    in FASTA format."""

    homepage = "https://github.com/davidemms/OrthoFinder"
    url      = "https://github.com/davidemms/OrthoFinder/releases/download/2.2.0/OrthoFinder-2.2.0.tar.gz"

    version('2.2.0', '4ff585e1eb148fc694a219296fbdd431')

    depends_on('blast-plus', type='run')
    depends_on('mcl', type='run')
    depends_on('fastme', type='run')
    depends_on('py-dlcpar', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.bin, 'orthofinder'))
