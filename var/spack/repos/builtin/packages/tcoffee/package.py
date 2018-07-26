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


class Tcoffee(MakefilePackage):
    """T-Coffee is a multiple sequence alignment program."""

    homepage = "http://www.tcoffee.org/"
    git      = "https://github.com/cbcrg/tcoffee.git"

    version('2017-08-17', commit='f389b558e91d0f82e7db934d9a79ce285f853a71')

    depends_on('perl', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('dialign-tx')
    depends_on('viennarna')
    depends_on('clustalw')
    depends_on('tmalign')
    depends_on('muscle')
    depends_on('mafft')
    depends_on('pcma')
    depends_on('poamsa')
    depends_on('probconsrna')

    build_directory = 'compile'

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('t_coffee')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('t_coffee', prefix.bin)
