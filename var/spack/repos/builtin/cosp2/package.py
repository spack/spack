##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import shutil
import glob


class Cosp2(MakefilePackage):
    """ Proxy Application. CoSP2 represents a sparse linear algebra
        parallel algorithm for calculating the density matrix in electronic
        tructure theory. The algorithm is based on a recursive second-order
        Fermi-Operator expansion method (SP2) and is tailored for density
        functional based tight-binding calculations of non-metallic systems
        tags : proxy-app
    """
    tags = ['proxy-app']
    homepage = "http://www.exmatex.org/cosp2.html"

    url = "https://github.com/exmatex/CoSP2/archive/master.tar.gz"
    version('master', git='https://github.com/exmatex/CoSP2.git',
            description='master')

    variant('precision', default=True,
            description='Flag to hold Precesion Status')
    variant('serial', default=True, description='Serial Build')
    variant('parallel', default=True, description='Build with MPI Support')

    depends_on('mpi', when='+parallel')

    build_directory = 'src-mpi'

    def edit(self, spec, prefix):
        with working_dir('src-mpi'):
            filter_file(r'^CC\s*=.*', 'CC = %s' % self.spec['mpi'].mpicc,
                        'Makefile.vanilla')
            if '+precision' in spec:
                filter_file('DOUBLE_PRECISION = O.*', 'DOUBLE_PRECISION = OFF',
                            'Makefile.vanilla')
            shutil.copy('Makefile.vanilla', 'Makefile')

    def install(self, spec, prefix):
        shutil.move('bin', prefix)
        mkdirp(prefix.examples)
        mkdirp(prefix.pots)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('LICENSE.md', prefix.doc)
        for files in glob.glob('examples/*.*'):
            install(files, prefix.examples)
        for files in glob.glob('pots/*.*'):
            install(files, prefix.examples)