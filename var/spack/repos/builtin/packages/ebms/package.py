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



class Ebms(Package):
    """This is a miniapp for the Energy Banding Monte Carlo (EBMC)
       neutron transportation simulation code.  It is adapted from a
       similar miniapp provided by Andrew Siegel, whose algorithm is
       described in [1], where only one process in a compute node
       is used, and the compute nodes are divided into memory nodes
       and tracking nodes.    Memory nodes do not participate in particle
       tracking. Obviously, there is a lot of resource waste in this design."""

    homepage = "http://www.example.com"
    url = "https://github.com/ANL-CESAR/EBMS/archive/master.tar.gz"

    tags = ['proxy-app']

    version('master', git='https://github.com/ANL-CESAR/EBMS.git')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        make()
        install('ebmc-iallgather', prefix.bin)
        install('ebmc-rget', prefix.bin)
