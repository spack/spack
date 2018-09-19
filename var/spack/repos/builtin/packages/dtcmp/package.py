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


class Dtcmp(Package):
    """The Datatype Comparison Library provides comparison operations and
       parallel sort algorithms for MPI applications."""

    homepage = "https://github.com/hpc/dtcmp"
    url      = "https://github.com/hpc/dtcmp/releases/download/v1.0.3/dtcmp-1.0.3.tar.gz"

    version('1.1.0', 'af5c73f7d3a9afd90a22d0df85471d2f')
    version('1.0.3', 'cdd8ccf71e8ff67de2558594a7fcd317')

    depends_on('mpi')
    depends_on('lwgrp')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-lwgrp=" + spec['lwgrp'].prefix)
        make()
        make("install")
