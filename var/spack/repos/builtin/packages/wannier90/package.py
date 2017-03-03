##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import inspect
import os.path
import shutil

from spack import *


class Wannier90(Package):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs).

    Wannier90 is released under the GNU General Public License.
    """
    homepage = 'http://wannier.org'
    url = 'http://wannier.org/code/wannier90-2.0.1.tar.gz'

    version('2.0.1', '4edd742506eaba93317249d33261fb22')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')

    parallel = False

    def install(self, spec, prefix):

        lapack = self.spec['lapack'].libs
        blas = self.spec['blas'].libs
        substitutions = {
            '@F90': spack_fc,
            '@MPIF90': self.spec['mpi'].mpifc,
            '@LIBS': (lapack + blas).joined()
        }
        #######
        # TODO : this part is replicated in PEXSI
        # TODO : and may be a common pattern for Editable Makefiles
        # TODO : see #1186
        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'make.sys'
        )
        makefile = join_path(
            self.stage.source_path,
            'make.sys'
        )

        shutil.copy(template, makefile)
        for key, value in substitutions.items():
            filter_file(key, value, makefile)
        ######

        make('wannier')
        mkdirp(self.prefix.bin)
        install(
            join_path(self.stage.source_path, 'wannier90.x'),
            join_path(self.prefix.bin, 'wannier90.x')
        )

        make('post')
        install(
            join_path(self.stage.source_path, 'postw90.x'),
            join_path(self.prefix.bin, 'postw90.x')
        )

        make('lib')
        mkdirp(self.prefix.lib)
        install(
            join_path(self.stage.source_path, 'libwannier.a'),
            join_path(self.prefix.lib, 'libwannier.a')
        )

        make('w90chk2chk')
        install(
            join_path(self.stage.source_path, 'w90chk2chk.x'),
            join_path(self.prefix.bin, 'w90chk2chk.x')
        )

        make('w90vdw')
        install(
            join_path(self.stage.source_path, 'utility', 'w90vdw', 'w90vdw.x'),
            join_path(self.prefix.bin, 'w90vdw.x')
        )

        make('w90pov')
        install(
            join_path(self.stage.source_path, 'utility', 'w90pov', 'w90pov'),
            join_path(self.prefix.bin, 'w90pov')
        )

        install_tree(
            join_path(self.stage.source_path, 'pseudo'),
            join_path(self.prefix.bin, 'pseudo')
        )
