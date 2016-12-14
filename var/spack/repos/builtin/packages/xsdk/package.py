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


class Xsdk(Package):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
       simulation. This is a Spack bundle package that installs the xSDK 
       packages
    """

    homepage = "http://xsdk.info"

    # Dummy url since Spack complains if I don't list something, will be
    # removed when metapackage is available
    url      = 'https://bitbucket.org/saws/saws/get/master.tar.gz'

    # Spack can not handle both the support and 0.2.0 so
    # comment out the 0.2.0 version
    # this is for testing with the master of each package
    version('develop', '941a541bdf625856be18c9752249146d')
    # this is for next planned release
    # version('0.2.0', '941a541bdf625856be18c9752249146d')

    # depends_on('hypre@2.11.1~internal-superlu', when='@0.2.0')
    depends_on('hypre@develop~internal-superlu')    

    # depends_on('superlu-dist@5.0.0', when='@0.2.0')    
    depends_on('superlu-dist@develop')    

    # depends_on('trilinos@12.6.2+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse', when='@0.2.0')
    depends_on('trilinos@develop+xsdkflags+hypre+superlu-dist+metis+hdf5~mumps+boost~suite-sparse')

    # depends_on('petsc@3.7.4+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps~boost', when='@0.2.0')
    depends_on('petsc@develop+trilinos+mpi+hypre+superlu-dist+metis+hdf5~mumps~boost')

    # depends_on('pflotran@0.2.0', when='@0.2.0')    
    depends_on('pflotran@develop')    

    depends_on('xsdktrilinos@develop')

    # How do we propagate debug flag to all depends on packages ?
    #   If I just do spack install xsdk+debug will that propogate it down?

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        # Prevent the error message
        #      ==> Error: Install failed for xsdk.  Nothing was installed!
        #      ==> Error: Installation process had nonzero exit code : 256
        with open(os.path.join(spec.prefix, 'bundle-package.txt'), 'w') as out:
            out.write('This is a bundle\n')
            out.close()
