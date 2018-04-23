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


class Daligner(MakefilePackage):
    """Daligner: The Dazzler "Overlap" Module."""

    homepage = "https://github.com/thegenemyers/DALIGNER"
    url      = "https://github.com/thegenemyers/DALIGNER/archive/V1.0.tar.gz"

    version('1.0', 'f1b4c396ae062caa4c0e6423ba0725ef')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': True}
        makefile.filter('cp $(ALL) ~/bin',
                        'cp $(ALL) {0}'.format(prefix.bin),
                        **kwargs)
        # He changed the Makefile in commit dae119.
        # You'll need this instead if/when he cuts a new release
        # or if you try to build from the tip of master.
        # makefile.filter('DEST_DIR = .*',
        #                'DEST_DIR = {0}'.format(prefix.bin))
        # or pass DEST_DIR in to the make

    @run_before('install')
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)
