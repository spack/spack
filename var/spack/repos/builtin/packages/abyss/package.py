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


class Abyss(AutotoolsPackage):
    """ABySS is a de novo, parallel, paired-end sequence assembler
       that is designed for short reads. The single-processor version
       is useful for assembling genomes up to 100 Mbases in size."""

    homepage = "http://www.bcgsc.ca/platform/bioinfo/software/abyss"
    url      = "https://github.com/bcgsc/abyss/releases/download/1.5.2/abyss-1.5.2.tar.gz"

    version('2.0.2', '1623f55ad7f4586e80f6e74b1f27c798')
    version('1.5.2', '10d6d72d1a915e618d41a5cbbcf2364c')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    depends_on('mpi')
    depends_on('boost@:1.50.0,1.53.0:', when='@2.0.2:')
    depends_on('boost@:1.50.0,1.53.0:1.59.0', when='@:1.5.2')
    depends_on('sparsehash')
    depends_on('sqlite')
    depends_on('libtool')

    conflicts('^intel-mpi')
    conflicts('^intel-parallel-studio+mpi')
    conflicts('^mvapich2')
    conflicts('^spectrum-mpi')

    def configure_args(self):
        args = ['--with-boost=%s' % self.spec['boost'].prefix,
                '--with-sqlite=%s' % self.spec['sqlite'].prefix,
                '--with-mpi=%s' % self.spec['mpi'].prefix]
        if self.spec['mpi'].name == 'mpich':
                args.append('--enable-mpich')
        return args
