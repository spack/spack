##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
    git      = "https://github.com/ANL-CESAR/SNbone.git"

    version('develop')

    tags = ['proxy-app']

    depends_on('metis')

    def build(self, spec, prefix):
        working_dirs = ['src_c', 'src_fortran', 'src_makemesh',
                        'src_processmesh']
        for wdir in working_dirs:
            with working_dir(wdir, create=False):
                if self.compiler.name == 'gcc' and wdir == 'src_processmesh':
                    make('COMPILER=gfortran', 'METISLIB={0}'
                         .format(spec['metis'].prefix + '/lib/libmetis.so'))
                elif self.compiler.name == 'intel':
                    make('COMPILER=intel', 'LDFLAGS=-lm')
                else:
                    # older gcc need link libs after objs, but
                    # LDFLAGS is in the front, so use IBMLIB instead
                    make('COMPILER=gfortran', 'IBMLIB=-lm')

    def install(self, spec, prefix):
        mkdirp(prefix.bin.C)
        mkdirp(prefix.bin.Fortran)
        mkdirp(prefix.bin.MakeMesh)
        mkdirp(prefix.bin.ProcessMesh)

        install('src_c/SNaCFE.x',                prefix.bin.C)
        install('src_fortran/SNaCFE.x',          prefix.bin.Fortran)
        install('src_makemesh/makemesh.x',       prefix.bin.MakeMesh)
        install('src_processmesh/processmesh.x', prefix.bin.ProcessMesh)
