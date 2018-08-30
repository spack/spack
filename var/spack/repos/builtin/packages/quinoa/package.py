##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Quinoa(CMakePackage):
    """Quinoa is a set of computational tools that enables research and
       numerical analysis in fluid dynamics. At this time it is a test-bed
       to experiment with various algorithms using fully asynchronous runtime
       systems.
    """

    homepage = "http://quinoacomputing.org"
    git      = "https://github.com/quinoacomputing/quinoa.git"

    version('develop', branch='master')

    depends_on('hdf5+mpi')
    depends_on("charm backend=mpi")
    depends_on("trilinos+exodus")
    depends_on("boost")
    depends_on("hypre~internal-superlu")
    depends_on("random123")
    depends_on("netlib-lapack+lapacke")
    depends_on("mad-numdiff")
    depends_on("h5part")
    depends_on("boostmplcartesianproduct")
    depends_on("tut")
    depends_on("pugixml")
    depends_on("pstreams")
    depends_on("pegtl")

    root_cmakelists_dir = 'src'
