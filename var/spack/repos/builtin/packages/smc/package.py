##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import glob


class Smc(MakefilePackage):
    """A minimalist high-order finite difference algorithm
    for combustion problems. It includes core discretizations
    for advection, diffusive transport and chemical kinetics.
    The models for computing diffusive transport coefficients
    have been replaced by a simplified approximation
    but the full structure of the discretization of
    the diffusive terms have been preserved."""

    homepage = "https://ccse.lbl.gov/ExaCT/index.html"
    url      = "https://ccse.lbl.gov/ExaCT/SMC.tar.gz"
    tags     = ['proxy-app']

    version('master', '94a4ea94abbc5e61397c2a4d1fb56ed6')

    variant(
        'mpi', default=True,
        description='Build with MPI support')
    variant(
        'openmp', default=True,
        description='Build with OpenMP support')
    variant(
        'debug', default=False,
        description='Build with debugging')
#   variant(
#       'mic', default=False,
#       description='Compile for Intel Xeon Phi')
    variant(
        'k_use_automatic', default=True,
        description='Some arrays in kernels.F90 will be automatic')

    depends_on('mpi', when='+mpi')
    depends_on('gmake', type='build')

    def edit(self, spec, prefix):
        makefile = FileFilter('GNUmakefile')
        if '~mpi' in spec:
            makefile.filter('MPI := t', '#')
        if '~openmp' in spec:
            makefile.filter('OMP := t', '#')
        if '+debug' in spec:
            makefile.filter('NDEBUG :=', '#')
        if '~k_use_automatic' in spec:
            makefile.filter('K_U.*:= t', '#')
        if self.compiler.name == 'intel':
            makefile.filter('COMP := .*', 'COMP := Intel')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.glob(join_path(self.build_directory, '*.exe'))
        for f in files:
            install(f, prefix.bin)
        install('inputs_SMC', prefix.bin)
        install('README', prefix)
        install('BoxLib.license.txt', prefix)