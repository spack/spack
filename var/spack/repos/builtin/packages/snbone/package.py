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

from spack import *


class Snbone(MakefilePackage):
    """This application targets the primary computational solve burden of a SN,
       continuous finite element based transport equation solver."""

    homepage = "https://github.com/ANL-CESAR/"
    url = "https://github.com/ANL-CESAR/SNbone.git"

    version('master', git='https://github.com/ANL-CESAR/SNbone.git')

    depends_on('metis')

    def edit(self, spec, prefix):

        working_dirs = ['src_c', 'src_fortran', 'src_makemesh',
                        'src_processmesh']

        for wdir in working_dirs:

            with working_dir(wdir, create=False):
                if self.compiler.name == 'gcc' and wdir == 'src_processmesh':
                    make('COMPILER=gfortran', 'METISLIB={0}'
                         .format(spec['metis'].prefix + '/lib/libmetis.so'))
                else:
                    make('COMPILER=gfortran', 'LDFLAGS={0}'.format('-lm'))

                if self.compiler.name == 'mpixlf90_r':
                    make('COMPILER=bgq', 'LDFLAGS={0}'.format('-lm'))
                if self.compiler.name == 'icc':
                    make('COMPILER=intel', 'LDFLAGS={0}'.format('-lm'))

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):

        dirs = ['/C', '/Fortran', '/MakeMesh', '/ProcessMesh']

        files = ['SNaCFE.x', '../src_fortran/SNaCFE.x',
                 '../src_makemesh/makemesh.x',
                 '../src_processmesh/processmesh.x']

        mkdir(prefix.bin)

        for idx, dir in enumerate(dirs):
            with working_dir('src_c', create=False):
                mkdir(prefix.bin + dir)
                install(files[idx], prefix.bin + dir)
