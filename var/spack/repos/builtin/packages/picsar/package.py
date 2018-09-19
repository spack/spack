##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC.
# Produced at the Los Alamos National Laboratory.
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
import pdb

class Picsar(MakefilePackage):
    """The Particle-In-Cell Scalable Application Resource (PICSAR) is a high performance repository intended to help scientists porting their Particle-In-Cell (PIC) codes to the next generation of exascale computers.

PICSAR exploits the three levels of parallelism that will be required to achieve good performances on future architectures: distributed memory parallelization (internode), shared memory parallelization (intranode) and vectorization.

PICSAR includes:

    A high performance library of highly optimized versions of the key functionalities of the PIC loop.
    A compact "mini-app" standalone code, which serves as a self-contained proxy that adequately portrays the computational loads and dataflow of more complex PIC codes.
    A Python wrapper for using PICSAR optimized routines with Python-driven codes.
    """

    homepage = "http://picsar.net"
    git      = "https://bitbucket.org/berkeleylab/picsar.git"

    version('develop', branch='PICSARlite')
    depends_on('mpi')    


    @property
    def build_targets(self):
        targets = []
	serial = '-j1'
	targets.append('FC={0}'.format(self.spec['mpi'].mpifc))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
	targets.append(format(serial))
        return targets
  
    def install(self, spec, prefix):
        install_tree('fortran_bin', prefix.fortran_bin)
        install_tree('examples', prefix.examples)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
	install('license.txt', prefix.doc)
