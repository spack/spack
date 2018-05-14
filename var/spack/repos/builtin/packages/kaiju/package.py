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


class Kaiju(MakefilePackage):
    """Kaiju is a program for the taxonomic classification
    of high-throughput sequencing reads."""

    homepage = "https://github.com/bioinformatics-centre/kaiju"
    url      = "https://github.com/bioinformatics-centre/kaiju/archive/v1.6.2.zip"

    version('1.6.2', '0bd85368954837aa31f3de8b87ea410b')

    build_directory = 'src'

    depends_on('perl-io-compress', type='run')
    depends_on('py-htseq', type='run')

    def edit(self, spec, prefix):
        # Replace ftp:// with https://
        makedb = FileFilter('util/makeDB.sh')
        makedb.filter('ftp://', 'https://', string=True)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
