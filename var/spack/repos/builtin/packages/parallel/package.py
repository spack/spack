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


class Parallel(AutotoolsPackage):
    """GNU parallel is a shell tool for executing jobs in parallel using
    one or more computers. A job can be a single command or a small
    script that has to be run for each of the lines in the input.
    """

    homepage = "http://www.gnu.org/software/parallel/"
    url      = "http://ftp.gnu.org/gnu/parallel/parallel-20170122.tar.bz2"

    version('20170122', 'c9f0ec01463dc75dbbf292fd8be5f1eb')
    version('20160422', '24621f684130472694333709bd4454cb')
    version('20160322', '4e81e0d36902ab4c4e969ee6f35e6e57')

    def check(self):
        # The Makefile has a 'test' target, but it does not work
        make('check')
