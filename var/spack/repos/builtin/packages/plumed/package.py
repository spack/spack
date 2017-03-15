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
import subprocess

from spack import *


class Plumed(AutotoolsPackage):
    """PLUMED is an open source library for free energy calculations in
    molecular systems which works together with some of the most popular
    molecular dynamics engines.

    Free energy calculations can be performed as a function of many order
    parameters with a particular focus on biological problems, using state
    of the art methods such as metadynamics, umbrella sampling and
    Jarzynski-equation based steered MD.

    The software, written in C++, can be easily interfaced with both fortran
    and C/C++ codes.
    """
    homepage = 'http://www.plumed.org/'
    url = 'https://github.com/plumed/plumed2/archive/v2.2.3.tar.gz'

    version('2.2.3', 'a6e3863e40aac07eb8cf739cbd14ecf8')

    # Variants. PLUMED by default builds a number of optional modules.
    # The ones listed here are not built by default for various reasons,
    # such as stability, lack of testing, or lack of demand.
    variant('crystallization', default=False,
            description='Build support for optional crystallization module.')
    variant('imd', default=False,
            description='Build support for optional imd module.')
    variant('manyrestraints', default=False,
            description='Build support for optional manyrestraints module.')
    variant('shared', default=True, description='Builds shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('gsl', default=True, description='Activates GSL support')

    # Dependencies. LAPACK and BLAS are recommended but not essential.
    depends_on('zlib')
    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')
    depends_on('gsl', when='+gsl')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    # Dictionary mapping PLUMED versions to the patches it provides
    # interactively
    plumed_patches = {
        '2.2.3': {
            'amber-14': '1',
            'gromacs-4.5.7': '2',
            'gromacs-4.6.7': '3',
            'gromacs-5.0.7': '4',
            'gromacs-5.1.2': '5',
            'lammps-6Apr13': '6',
            'namd-2.8': '7',
            'namd-2.9': '8',
            'espresso-5.0.2': '9'
        }
    }

    force_autoreconf = True

    def apply_patch(self, other):
        plumed = subprocess.Popen(
            [join_path(self.spec.prefix.bin, 'plumed'), 'patch', '-p'],
            stdin=subprocess.PIPE
        )
        opts = Plumed.plumed_patches[str(self.version)]
        search = '{0.name}-{0.version}'.format(other)
        choice = opts[search] + '\n'
        plumed.stdin.write(choice)
        plumed.wait()

    def setup_dependent_package(self, module, dependent_spec):
        # Make plumed visible from dependent packages
        module.plumed = Executable(join_path(self.spec.prefix.bin, 'plumed'))

    @run_before('autoreconf')
    def filter_gslcblas(self):
        # This part is needed to avoid linking with gsl cblas
        # interface which will mask the cblas interface
        # provided by optimized libraries due to linking order
        filter_file('-lgslcblas', '', 'configure.ac')

    def configure_args(self):
        spec = self.spec

        # From plumed docs :
        # Also consider that this is different with respect to what some other
        # configure script does in that variables such as MPICXX are
        # completely ignored here. In case you work on a machine where CXX is
        # set to a serial compiler and MPICXX to a MPI compiler, to compile
        # with MPI you should use:
        #
        # > ./configure CXX="$MPICXX"
        configure_opts = []
        # If using MPI then ensure the correct compiler wrapper is used.
        if '+mpi' in spec:
            configure_opts.extend([
                '--enable-mpi',
                'CXX={0}'.format(spec['mpi'].mpicxx)
            ])

            # If the MPI dependency is provided by the intel-mpi package then
            # the following additional argument is required to allow it to
            # build.
            if spec.satisfies('^intel-mpi'):
                configure_opts.extend([
                    'STATIC_LIBS=-mt_mpi'
                ])

        # Additional arguments
        configure_opts.extend([
            '--enable-shared={0}'.format('yes' if '+shared' in spec else 'no'),
            '--enable-gsl={0}'.format('yes' if '+gsl' in spec else 'no')
        ])

        # Construct list of optional modules
        module_opts = []
        module_opts.extend([
            '+crystallization' if (
                '+crystallization' in spec) else '-crystallization',
            '+imd' if '+imd' in spec else '-imd',
            '+manyrestraints' if (
                '+manyrestraints' in spec) else '-manyrestraints'
        ])

        # If we have specified any optional modules then add the argument to
        # enable or disable them.
        if module_opts:
            configure_opts.extend([
                '--enable-modules={0}'.format("".join(module_opts))])

        return configure_opts
