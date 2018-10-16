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


class Turbine(AutotoolsPackage):
    """Turbine: The Swift/T runtime"""

    homepage = 'http://swift-lang.org/Swift-T'
    url      = 'http://swift-lang.github.io/swift-t-downloads/spack/turbine-0.0.0.tar.gz'

    version('1.2.3', 'f2e393c292c4248b4e77a19f8272ae88')
    version('1.2.1', 'c8976b22849aafe02a8fb4259dfed434')
    version('1.1.0', '9a347cf16df02707cb529f96c265a082')

    variant('python', default=False,
            description='Enable calling python')
    variant('r', default=False,
            description='Enable calling R')
    depends_on('adlbx@:0.8.0', when='@:1.1.0')
    depends_on('adlbx', when='@1.2.1:')
    depends_on('adlbx')
    depends_on('tcl', type=('build', 'run'))
    depends_on('zsh', type=('build', 'run'))
    depends_on('swig', type='build')
    depends_on('python', when='+python')
    depends_on('r', when='+r')

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('CXX', spec['mpi'].mpicxx)
        spack_env.set('CXXLD', spec['mpi'].mpicxx)

    def configure_args(self):
        args = ['--with-c-utils=' + self.spec['exmcutils'].prefix,
                '--with-adlb='    + self.spec['adlbx'].prefix,
                '--with-tcl='     + self.spec['tcl'].prefix,
                '--with-mpi='     + self.spec['mpi'].prefix]
        if '+python' in self.spec:
            args.append('--with-python-exe={0}'.format(
                        self.spec['python'].command.path))
        if '+r' in self.spec:
            args.append('--with-r={0}/rlib/R'.format(
                        self.spec['r'].prefix))
        return args
