##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Prokka(Package):
    """Prokka is a software tool to annotate bacterial, archaeal and viral
    genomes quickly and produce standards-compliant output files."""

    homepage = "https://github.com/tseemann/prokka"
    url      = "https://github.com/tseemann/prokka/archive/v1.12.tar.gz"

    version('1.13', '168193a4c61263759784564581523640')
    version('1.12', '658c4c203ddded3623e68a36f94cabec')

    depends_on('aragorn', type='run')
    depends_on('blast-plus', type='run')
    depends_on('hmmer', type='run')
    depends_on('infernal', type='run')
    depends_on('minced', type='run')
    depends_on('parallel', type='run')
    depends_on('perl', type='run')
    depends_on('perl-bio-perl', type='run')
    depends_on('perl-html-parser', type='run')
    depends_on('perl-swissknife', type='run')
    depends_on('perl-text-unidecode', type='run')
    depends_on('perl-time-piece', type='run')
    depends_on('perl-xml-simple', type='run')
    depends_on('prodigal', type='run')
    depends_on('signalp', type='run')
    depends_on('tbl2asn', type='run')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('db', prefix.db)
