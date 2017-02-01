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


class Netgauge(AutotoolsPackage):
    """Netgauge is a high-precision network parameter measurement
    tool. It supports benchmarking of many different network protocols
    and communication patterns. The main focus lies on accuracy,
    statistical analysis and easy extensibility.
    """
    homepage = "http://unixer.de/research/netgauge/"
    url      = "http://unixer.de/research/netgauge/netgauge-2.4.6.tar.gz"

    version('2.4.6', 'e0e040ec6452e93ca21ccc54deac1d7f')

    depends_on("mpi")
