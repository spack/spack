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
import glob


class Aspa(MakefilePackage):
    """A fundamental premise in ExMatEx is that scale-bridging performed in
    heterogeneous MPMD materials science simulations will place important
    demands upon the exascale ecosystem that need to be identified and
    quantified.
    """

    homepage = "http://www.exmatex.org/aspa.html"
    git      = "https://github.com/exmatex/ASPA.git"

    tags = ['proxy-app']

    version('master', branch='master')

    variant('mpi', default=True, description='Build with MPI Support')

    depends_on('lapack')
    depends_on('blas')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5')

    @property
    def build_targets(self):
        targets = [
            '--directory=exec',
            '--file=Makefile',
            'LIBS={0} {1} {2}'.format(self.spec['lapack'].libs.ld_flags,
                                      self.spec['blas'].libs.ld_flags,
                                      self.spec['hdf5'].libs.ld_flags),
            'CXX={0}'.format(self.spec['mpi'].mpicxx)
        ]
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)
        mkdirp(prefix.input)
        install('exec/aspa', prefix.bin)
        install('exec/README', prefix.doc)
        install('exec/aspa.inp', prefix.input)
        install('exec/kriging_model_centers.txt', prefix.input)
        install('exec/point_data.txt', prefix.input)
        install('exec/value_data.txt', prefix.input)
        for files in glob.glob('doc/*.*'):
            install(files, prefix.doc)
