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


class Fermisciencetools(Package):
    """The Fermi Science Tools consists of the basic tools necessary to
    analyze Fermi data.

    This is the binary version for Linux x86_64 with libc-2.17."""

    homepage = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/"
    url      = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/v11r5p3/ScienceTools-v11r5p3-fssc-20180124-x86_64-unknown-linux-gnu-libc2.17.tar.gz"

    # Now we are using the binary distribution. The source distribution is also
    # available, but there might be some logical errors in the configure codes,
    # which leads to failing in building it from source. Hopefully someone else
    # can figure it out and we can use the source distribution instead.
    version('11r5p3', 'cf050ddddfe9251b6ebe8d3fd7de3c3f')

    def install(self, spec, prefix):
        install_tree('x86_64-unknown-linux-gnu-libc2.17', prefix)
