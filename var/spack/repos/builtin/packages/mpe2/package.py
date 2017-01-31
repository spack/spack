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


class Mpe2(Package):
    """Message Passing Extensions (MPE): Parallel, shared X window graphics"""

    homepage = "http://www.mcs.anl.gov/research/projects/perfvis/software/MPE/"
    url      = "http://ftp.mcs.anl.gov/pub/mpi/mpe/mpe2-1.3.0.tar.gz"

    version('1.3.0', '67bf0c7b2e573df3ba0d2059a96c2f7b')

    patch('mpe2.patch')

    depends_on("mpi")

    provides("mpe")

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--x-includes=/usr/X11R6/include",
                  "--x-libraries=/usr/X11R6/lib",
                  "--enable-mpe_graphics=yes",
                  "--disable-f77",
                  "--enable-viewers=no",
                  "--enable-slog2=no",
                  "--with-mpicc=mpicc")

        make()
        make("install")
