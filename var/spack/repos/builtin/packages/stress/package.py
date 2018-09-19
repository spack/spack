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


class Stress(AutotoolsPackage):
    """stress is a deliberately simple workload generator for POSIX systems.
    It imposes a configurable amount of CPU, memory, I/O, and disk stress on
    the system. It is written in C, and is free software licensed under the
    GPLv2."""

    homepage = "https://people.seas.harvard.edu/~apw/stress/"
    url      = "https://people.seas.harvard.edu/~apw/stress/stress-1.0.4.tar.gz"

    version('1.0.4', '890a4236dd1656792f3ef9a190cf99ef')
