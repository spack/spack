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


class Mpifileutils(Package):
    """mpiFileUtils is a suite of MPI-based tools to manage large datasets,
       which may vary from large directory trees to large files.
       High-performance computing users often generate large datasets with
       parallel applications that run with many processes (millions in some
       cases). However those users are then stuck with single-process tools
       like cp and rm to manage their datasets. This suite provides
       MPI-based tools to handle typical jobs like copy, remove, and compare
       for such datasets, providing speedups of up to 20-30x."""

    homepage = "https://github.com/hpc/mpifileutils"
    url      = "https://github.com/hpc/mpifileutils/releases/download/v0.6/mpifileutils-0.6.tar.gz"

    version('0.6', '620bcc4966907481f1b1a965b28fc9bf')

    depends_on('mpi')
    depends_on('libcircle')
    depends_on('lwgrp')
    depends_on('dtcmp')
    depends_on('libarchive')

    variant('lustre', default=False)

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-lwgrp=" + spec['lwgrp'].prefix)

        make_args = []
        if '+lustre' in spec:
            make_args.append('CFLAGS=-DDCOPY_USE_XATTRS')

        make(", ".join(make_args))
        make("install")
