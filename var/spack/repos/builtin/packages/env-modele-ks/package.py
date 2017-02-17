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


class EnvModeleKs(Package):
    """ModelE "kitchen sink" environment."""

    homepage = ""

    version('1.0', 'e2b724dfcc31d735897971db91be89ff')

    variant('python', default=True,
            description='Include basic scientific Python environment')

    # Utilities
    depends_on('emacs')
    depends_on('git')

    # --------- ModelE dependencies (taken from modele/package.py)
    # Build dependencies
    depends_on('m4')
    depends_on('cmake@3.2:')
    # Link dependencies
    depends_on('mpi')
    depends_on('netcdf-fortran')
    #depends_on('fexception')
    depends_on('everytrace+fortran+mpi')
    depends_on('parallel-netcdf+fortran~cxx')

    # -------- Other things we need
    depends_on('modele-utils')
    depends_on('ncview')
    depends_on('nco')

    # Running ModelE
#    depends_on('modele-control')



# These cause invalid spec...



    def url_for_version(self, version):
        return 'https://github.com/citibeth/dummy/tarball/v1.0'

    def install(self, spec, prefix):
        with open(os.path.join(spec.prefix, 'dummy.txt'), 'w') as out:
            out.write('This is a bundle\n')

