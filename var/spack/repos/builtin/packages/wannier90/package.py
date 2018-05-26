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
import inspect
import os.path

from spack import *


class Wannier90(MakefilePackage):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs).

    Wannier90 is released under the GNU General Public License.
    """
    homepage = 'http://wannier.org'
    url = 'http://wannier.org/code/wannier90-2.0.1.tar.gz'

    version('2.1.0', '07a81c002b41d6d0f97857e55c57d769')
    version('2.0.1', '4edd742506eaba93317249d33261fb22')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')

    parallel = False

    build_targets = [
        'wannier', 'post', 'lib', 'w90chk2chk', 'w90vdw', 'w90pov'
    ]

    @property
    def makefile_name(self):
        # Older versions use 'make.sys'
        filename = 'make.sys'

        # While newer search for 'make.inc'
        if self.spec.satisfies('@2.1.0:'):
            filename = 'make.inc'

        abspath = join_path(self.stage.source_path, filename)
        return abspath

    def edit(self, spec, prefix):

        lapack = self.spec['lapack'].libs
        blas = self.spec['blas'].libs
        substitutions = {
            '@F90': spack_fc,
            '@MPIF90': self.spec['mpi'].mpifc,
            '@LIBS': (lapack + blas).joined()
        }

        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'make.sys'
        )

        copy(template, self.makefile_name)
        for key, value in substitutions.items():
            filter_file(key, value, self.makefile_name)

    def install(self, spec, prefix):

        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.lib)

        install(
            join_path(self.stage.source_path, 'wannier90.x'),
            join_path(self.prefix.bin, 'wannier90.x')
        )

        install(
            join_path(self.stage.source_path, 'postw90.x'),
            join_path(self.prefix.bin, 'postw90.x')
        )

        install(
            join_path(self.stage.source_path, 'libwannier.a'),
            join_path(self.prefix.lib, 'libwannier.a')
        )

        install(
            join_path(self.stage.source_path, 'w90chk2chk.x'),
            join_path(self.prefix.bin, 'w90chk2chk.x')
        )

        install(
            join_path(self.stage.source_path, 'utility', 'w90vdw', 'w90vdw.x'),
            join_path(self.prefix.bin, 'w90vdw.x')
        )

        install(
            join_path(self.stage.source_path, 'utility', 'w90pov', 'w90pov'),
            join_path(self.prefix.bin, 'w90pov')
        )

        install_tree(
            join_path(self.stage.source_path, 'pseudo'),
            join_path(self.prefix.bin, 'pseudo')
        )
