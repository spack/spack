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


class Tracer(MakefilePackage):
    """Trace Replay and Network Simulation Framework"""

    homepage = "https://tracer-codes.readthedocs.io"
    git      = "https://github.com/LLNL/tracer.git"

    maintainers = ['bhatele']

    version('develop', branch='master')

    variant('otf2', default=True, description='Use OTF2 traces for simulation')

    depends_on('mpi')
    depends_on('codes')
    depends_on('otf2', when='+otf2')

    build_directory = 'tracer'

    @property
    def build_targets(self):
        targets = []

        targets.append('CXX = {0}'.format(self.spec['mpi'].mpicxx))
        if "+otf2" in self.spec:
            targets.append('SELECT_TRACE = -DTRACER_OTF_TRACES=1')

        return targets

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('PREFIX={0}'.format(prefix), 'install')
