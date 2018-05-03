##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Phast(MakefilePackage):
    """PHAST is a freely available software package for comparative and
       evolutionary genomics."""

    homepage = "http://compgen.cshl.edu/phast/index.php"
    url      = "https://github.com/CshlSiepelLab/phast/archive/v1.4.tar.gz"

    version('1.4', '2bc0412ba58ea1f08ba5e12fad43b4c7')

    # phast cannot build with clapack using external blas
    depends_on('clapack~external-blas')

    build_directory = 'src'

    @property
    def build_targets(self):
        targets = ['CLAPACKPATH={0}'.format(self.spec['clapack'].prefix)]
        return targets

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file(r'\$\{PWD\}',
                        '$(dir $(realpath $(firstword $(MAKEFILE_LIST))))',
                        'make-include.mk')
            filter_file(r'\$\{PWD\}',
                        '$(dir $(realpath $(firstword $(MAKEFILE_LIST))))',
                        'Makefile')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
