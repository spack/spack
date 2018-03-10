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

import os
from spack import *

class Ceed(Package):
    """Ceed is a suite of Department of Energy (DOE) packages partially
       supported by the Exascale Computing Project (ECP). This is a Spack
       bundle package that installs the CEED packages
    """

    homepage = "https://github.com/llnl/ceed"

    # Dummy url since Spack complains if I don't list something, will be
    # removed when metapackage is available
    url      = 'https://bitbucket.org/saws/saws/get/master.tar.gz'

    version('1.0.0', 'a52dc710c744afa0b71429b8ec9425bc')

    variant('cuda', default=False, description='Enable CUDA dependent packages')

    depends_on('gslib@1.0.1', when='@1.0.0')
    depends_on('hpgmg@a0a5510+fe', when='@1.0.0')
    depends_on('laghos@1.0', when='@1.0.0')
    depends_on('libceed@0.1+occa', when='@1.0.0 +cuda')
    depends_on('magma@2.2.0', when='@1.0.0 +cuda')
    depends_on('mfem@3.3.2+mpi+hypre+superlu-dist+petsc+examples+miniapps', when='@1.0.0')
    depends_on('nek5000@17.0', when='@1.0.0')
    depends_on('nekbone@17.0', when='@1.0.0')
    depends_on('nekcem@0b8bedd', when='@1.0.0')
    depends_on('petsc@3.8.3+mpi+hypre+superlu-dist+metis+hdf5+mumps+boost+double~int64', when='@1.0.0')
    depends_on('pumi@2.1.0', when='@1.0.0')
    depends_on('occa@0.2', when='@1.0.0 +cuda')

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        # Prevent the error message
        #      ==> Error: Install failed for ceed.  Nothing was installed!
        #      ==> Error: Installation process had nonzero exit code : 256
        with open(os.path.join(spec.prefix, 'bundle-package.txt'), 'w') as out:
            out.write('This is a bundle\n')
            out.close()
