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


class PacbioDextractor(MakefilePackage):
    """The Dextractor and Compression Command Library. This is a special
       fork required by some pacbio utilities."""

    homepage = "https://github.com/PacificBiosciences/DEXTRACTOR"
    git      = "https://github.com/PacificBiosciences/DEXTRACTOR.git"

    version('2016-08-09', commit='89726800346d0bed15d98dcc577f4c7733aab4b1')

    depends_on('hdf5')
    depends_on('gmake', type='build')

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter('Makefile')
        makefile.filter('PATH_HDF5\s*=\s*/sw/apps/hdf5/current',
                        'PATH_HDF5 = ' + spec['hdf5'].prefix)
        makefile.filter('PATH_HDF5\*s=\s*/usr/local/hdf5', '')
        makefile.filter('DEST_DIR\s*=\s*~/bin', 'DEST_DIR = ' + prefix.bin)
        gmf = FileFilter('GNUmakefile')
        gmf.filter('rsync\s*-av\s*\$\{ALL\}\s*\$\{PREFIX\}/bin',
                   'cp ${ALL} ' + prefix.bin)
