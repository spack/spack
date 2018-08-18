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


class Chatterbug(MakefilePackage):
    """A suite of communication-intensive proxy applications that mimic
       commonly found communication patterns in HPC codes. These codes can be
       used as synthetic codes for benchmarking, or for trace generation using
       Score-P / OTF2.
    """
    tags = ['proxy-app']

    homepage = "https://chatterbug.readthedocs.io"
    git      = "https://github.com/LLNL/chatterbug.git"

    version('develop', branch='master')
    version('1.0', tag='v1.0')

    variant('scorep', default=False, description='Build with Score-P tracing')

    depends_on('mpi')
    depends_on('scorep', when='+scorep')

    @property
    def build_targets(self):
        targets = []

        targets.append('MPICXX = {0}'.format(self.spec['mpi'].mpicxx))

        return targets

    def build(self, spec, prefix):
        if "+scorep" in spec:
            make('WITH_OTF2=YES')
        else:
            make()

    def install(self, spec, prefix):
        if "+scorep" in spec:
            make('WITH_OTF2=YES', 'PREFIX=' + spec.prefix, 'install')
        else:
            make('PREFIX=' + spec.prefix, 'install')
