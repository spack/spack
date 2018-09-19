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


class PyAdios(PythonPackage):
    """NumPy bindings of ADIOS1"""

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git      = "https://github.com/ornladios/ADIOS.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('1.13.0', '68af36b821debbdf4748b20320a990ce')
    version('1.12.0', '84a1c71b6698009224f6f748c5257fc9')
    version('1.11.1', '5639bfc235e50bf17ba9dafb14ea4185')
    version('1.11.0', '5eead5b2ccf962f5e6d5f254d29d5238')
    version('1.10.0', 'eff450a4c0130479417cfd63186957f3')
    version('1.9.0', '310ff02388bbaa2b1c1710ee970b5678')

    variant('mpi', default=True,
            description='Enable MPI support')

    for v in ['1.9.0', '1.10.0', '1.11.0', '1.11.1', '1.12.0', '1.13.0',
              'develop']:
        depends_on('adios@{0} ~mpi'.format(v),
                   when='@{0} ~mpi'.format(v),
                   type=['build', 'link', 'run'])
        depends_on('adios@{0} +mpi'.format(v),
                   when='@{0} +mpi'.format(v),
                   type=['build', 'link', 'run'])

    depends_on('py-numpy', type=['build', 'run'])
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', type=['run'], when='+mpi')
    depends_on('py-cython', type=['build'])

    phases = ['build_clib', 'install']
    build_directory = 'wrappers/numpy'

    def setup_file(self):
        """Returns the name of the setup file to use."""
        if '+mpi' in self.spec:
            return 'setup_mpi.py'
        else:
            return 'setup.py'

    def build_clib(self, spec, prefix):
        # calls: make [MPI=y] python
        args = ''
        if '+mpi' in self.spec:
            args = 'MPI=y '
        args += 'python'
        with working_dir(self.build_directory):
            make(args)
