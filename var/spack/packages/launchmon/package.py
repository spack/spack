##############################################################################
# Copyright (c) 2014, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Matthew LeGendre, legendre1@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Launchmon(Package):
    """Software infrastructure that enables HPC run-time tools to
       co-locate tool daemons with a parallel job."""
    homepage = "http://sourceforge.net/projects/launchmon"
    url      = "http://downloads.sourceforge.net/project/launchmon/launchmon/1.0.1%20release/launchmon-1.0.1.tar.gz"

    version('1.0.1', '2f12465803409fd07f91174a4389eb2b')
    version('1.0.1-2', git='https://github.com/scalability-llnl/launchmon.git', commit='ff7e22424b8f375318951eb1c9282fcbbfa8aadf')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')

    def install(self, spec, prefix):
        configure(
            "--prefix=" + prefix,
            "--with-bootfabric=cobo",
            "--with-rm=slurm")

        make()
        make("install")
