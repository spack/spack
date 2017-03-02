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


class Launchmon(Package):
    """Software infrastructure that enables HPC run-time tools to
       co-locate tool daemons with a parallel job."""
    homepage = "https://github.com/LLNL/LaunchMON"
    url = "https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz"

    version('1.0.2', '8d6ba77a0ec2eff2fde2c5cc8fa7ff7a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('libgcrypt')
    depends_on('libgpg-error')
    depends_on("elf", type='link')
    depends_on("boost")
    depends_on("spectrum-mpi", when='arch=ppc64le')

    def install(self, spec, prefix):
        configure(
            "--prefix=" + prefix,
            "--with-bootfabric=cobo",
            "--with-rm=slurm")

        make()
        make("install")
