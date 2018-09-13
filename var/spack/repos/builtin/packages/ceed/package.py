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
from spack import *
import os


class Ceed(Package):
    """Ceed is a collection of benchmarks, miniapps, software libraries and
       APIs for efficient high-order finite element and spectral element
       discretizations for exascale applications developed in the Department of
       Energy (DOE) and partially supported by the Exascale Computing Project
       (ECP). This is a Spack bundle package that installs the CEED software
       components."""

    homepage = "https://ceed.exascaleproject.org"

    url  = 'file://' + os.path.dirname(__file__) + '/README.md'
    sha1 = 'b2eefd95c09ba573f663a761b84811a2d7e39788'

    version('1.0.0', sha1, expand=False)

    variant('cuda', default=False,
            description='Build MAGMA; enable CUDA support in libCEED and OCCA')
    variant('mfem', default=True, description='Build MFEM and Laghos')
    variant('nek', default=True,
            description='Build Nek5000, GSLIB, Nekbone, and NekCEM')
    variant('occa', default=True,
            description='Build OCCA; enable OCCA support in libCEED')
    variant('petsc', default=True,
            description='Build PETSc and HPGMG')
    variant('pumi', default=True,
            description='Build PUMI')
    variant('quickbuild', default=True,
            description='Speed-up the build by disabling variants in packages')
    # TODO: Add 'int64' variant?

    # LibCEED
    depends_on('libceed@0.2~cuda', when='@1.0.0~cuda')
    depends_on('libceed@0.2+cuda', when='@1.0.0+cuda')
    depends_on('libceed@0.2+occa', when='@1.0.0+occa')
    depends_on('libceed@0.2~occa', when='@1.0.0~occa')

    # OCCA
    depends_on('occa@v1.0.0-alpha.5~cuda', when='@1.0.0+occa~cuda')
    depends_on('occa@v1.0.0-alpha.5+cuda', when='@1.0.0+occa+cuda')

    # Nek5000, GSLIB, Nekbone, and NekCEM
    depends_on('nek5000@17.0', when='@1.0.0+nek')
    depends_on('gslib@1.0.2', when='@1.0.0+nek')
    depends_on('nekbone@17.0', when='@1.0.0+nek')
    depends_on('nekcem@0b8bedd', when='@1.0.0+nek')

    # PETSc, HPGMG
    # For a +quickbuild we disable hdf5, and superlu-dist in PETSc.
    # Ideally, these can be turned into recommendations to Spack for
    # concretizing the PETSc spec, if Spack ever supports recommendations.
    depends_on('petsc@3.8.3~hdf5~superlu-dist',
               when='@1.0.0+petsc+quickbuild')
    depends_on('petsc@3.8.3+mpi+double~int64', when='@1.0.0+petsc~mfem')
    # The mfem petsc examples need the petsc variants +hypre, +suite-sparse,
    # and +mumps:
    depends_on('petsc@3.8.3+mpi+hypre+suite-sparse+mumps+double~int64',
               when='@1.0.0+petsc+mfem')
    depends_on('hpgmg@a0a5510df23b+fe', when='@1.0.0+petsc')

    # MAGMA
    depends_on('magma@2.3.0', when='@1.0.0+cuda')

    # PUMI
    depends_on('pumi@2.1.0', when='@1.0.0+pumi')

    # MFEM, Laghos
    depends_on('mfem@3.3.2+mpi+examples+miniapps', when='@1.0.0+mfem~petsc')
    depends_on('mfem@3.3.2+mpi+petsc+examples+miniapps',
               when='@1.0.0+mfem+petsc')
    depends_on('laghos@1.0', when='@1.0.0+mfem')
    # The next line seems to be necessary because the concretizer somehow
    # decides that mfem requires 'hypre+internal-superlu' even though the mfem
    # package lists simply 'hypre' as dependency. This is only an issue because
    # petsc explicitly requires 'hypre~internal-superlu' which for the
    # concretizer is a conflict.
    depends_on('hypre~internal-superlu', when='@1.0.0+mfem')

    # If using gcc version <= 4.8 build suite-sparse version <= 5.1.0
    depends_on('suite-sparse@:5.1.0', when='@1.0.0%gcc@:4.8+mfem+petsc')

    # Dummy install
    def install(self, spec, prefix):
        install('README.md', prefix)
