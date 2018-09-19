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
import os
from spack import *


class Rockstar(MakefilePackage):
    """The Rockstar Halo Finder"""

    homepage = "https://bitbucket.org/gfcstanford/rockstar"

    version('develop', git='https://bitbucket.org/gfcstanford/rockstar.git')
    version('yt', hg='https://bitbucket.org/MatthewTurk/rockstar')

    variant('hdf5', description='Build rockstar with HDF5 support', default=False)

    patch('adjust_buildscript.patch')

    depends_on('hdf5', when='+hdf5')

    def build(self, spec, prefix):
        # Set environment appropriately for HDF5
        if '+hdf5' in spec:
            os.environ['HDF5_INC_DIR'] = spec['hdf5'].prefix.include
            os.environ['HDF5_LIB_DIR'] = spec['hdf5'].prefix.lib

        # Build depending on whether hdf5 is to be used
        if '+hdf5' in spec:
            make('with_hdf5')
        else:
            make()

        # Build rockstar library
        make('lib')

    def install(self, spec, prefix):
        # Install all files and directories
        install_tree('.', prefix)

        mkdir(prefix.bin)
        mkdir(prefix.lib)

        install('rockstar', join_path(prefix.bin, 'rockstar'))
        install('librockstar.so', join_path(prefix.lib, 'librockstar.so'))
