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


class Heppdt(AutotoolsPackage):
    """The HepPID library contains translation methods for particle ID's
    to and from various Monte Carlo generators and the PDG standard
    numbering scheme. We realize that the generators adhere closely
    to the standard, but there are occasional differences."""
    homepage = "http://lcgapp.cern.ch/project/simu/HepPDT/"
    url      = "http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-2.06.01.tar.gz"

    version('3.04.01', 'a8e93c7603d844266b62d6f189f0ac7e')
    version('3.04.00', '2d2cd7552d3e9539148febacc6287db2')
    version('3.03.02', '0b85f1809bb8b0b28a46f23c718b2773')
    version('3.03.01', 'd411f3bfdf9c4350d802241ba2629cc2')
    version('3.03.00', 'cd84d0a0454be982dcd8c285e060a7b3')
    version('2.06.01', '5688b4bdbd84b48ed5dd2545a3dc33c0')
