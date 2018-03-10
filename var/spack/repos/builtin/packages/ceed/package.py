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
    """Ceed is a suite of Department of Energy (DOE) packages partially
       supported by the Exascale Computing Project (ECP). This is a Spack
       bundle package that installs the CEED packages
    """

    homepage = "https://ceed.exascaleproject.org/"

    # Dummy url since Spack complains if we don't list something, will be
    # removed when metapackage is available.
    url      = 'file:///dev/null'
    sha1     = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

    version('1.0.0', sha1, expand=False)

    variant('cuda', default=False, description='Enable CUDA dependent packages')
    # TODO: Add 'int64' variant?

    depends_on('gslib@1.0.1', when='@1.0.0')
    depends_on('hpgmg@a0a5510+fe', when='@1.0.0')
    depends_on('laghos@1.0', when='@1.0.0')
    # FIXME: Make a v0.2 release of libceed from the current master?
    depends_on('libceed@0.1+occa', when='@1.0.0')
    depends_on('magma@2.2.0', when='@1.0.0 +cuda')
    # The next line seems to be necessary because the concretizer somehow
    # decides that mfem requires 'hypre+internal-superlu' even though the mfem
    # package lists simply 'hypre' as dependency. This is only an issue because
    # petsc explicitly requires 'hypre~internal-superlu' which for the
    # concretizer is a conflict.
    depends_on('hypre~internal-superlu')
    depends_on('mfem@3.3.2+mpi+petsc+examples+miniapps', when='@1.0.0')
    depends_on('nek5000@17.0', when='@1.0.0')
    depends_on('nekbone@17.0', when='@1.0.0')
    depends_on('nekcem@0b8bedd', when='@1.0.0')
    # The mfem petsc examples need the petsc variants '+suite-sparse+mumps':
    depends_on('petsc@3.8.3+mpi+hypre+suite-sparse+metis+hdf5+mumps~boost'
               '+double~int64', when='@1.0.0')
    depends_on('pumi@2.1.0', when='@1.0.0')
    # FIXME: pick a fixed occa version:
    depends_on('occa@develop+cuda', when='@1.0.0+cuda')
    depends_on('occa@develop~cuda', when='@1.0.0~cuda')

    # Dummy install for now, will be removed when metapackage is available.
    def install(self, spec, prefix):
        # Prevent the error message
        #      ==> Error: Install failed for ceed.  Nothing was installed!
        #      ==> Error: Installation process had nonzero exit code : 256
        with open(os.path.join(spec.prefix, 'bundle-package.txt'), 'w') as out:
            out.write('This is a bundle\n')
            out.close()
