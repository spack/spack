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

import glob
import tarfile

from spack import *


class Minimd(MakefilePackage):
    """Proxy Application. A simple proxy for the force computations
       in a typical molecular dynamics applications.
    """

    homepage = "http://mantevo.org"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniMD/miniMD_1.2.tgz"

    tags = ['proxy-app']

    version('1.2', '893ef1ca5062e32b43a8d11bcfe1a056')

    depends_on('mpi')

    build_directory = 'miniMD_ref'

    @property
    def build_targets(self):
        targets = [
            'LINK={0}'.format(self.spec['mpi'].mpicxx),
            'CC={0}'.format(self.spec['mpi'].mpicxx),
            'CCFLAGS={0} -DMPICH_IGNORE_CXX_SEEK -DNOCHUNK'.format(
                self.compiler.openmp_flag),
            'EXE=miniMD_mpi',
            'openmpi'
        ]

        return targets

    def edit(self, spec, prefix):
        inner_tar = tarfile.open(name='miniMD_{0}_ref.tgz'.format(
                                 self.version.up_to(2)))
        inner_tar.extractall()

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('miniMD_ref/miniMD_mpi', prefix.bin)
        install('miniMD_ref/in.lj.miniMD', prefix.bin)
        install('miniMD_ref/README', prefix.doc)

        for f in glob.glob('miniMD_ref/in.*'):
            install(f, prefix.doc)
