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


class Discovardenovo(AutotoolsPackage):
    """DISCOVAR de novo is a large (and small) de novo genome assembler.
       It quickly generates highly accurate and complete assemblies using the
       same single library data as used by DISCOVAR. It currently doesn't
       support variant calling, for that, please use DISCOVAR instead."""

    homepage = "https://software.broadinstitute.org/software/discovar/blog/"
    url      = "ftp://ftp.broadinstitute.org/pub/crd/DiscovarDeNovo/latest_source_code/discovardenovo-52488.tar.gz"

    version('52488', '2b08c77b1b998d85be8048e5efb10358')

    # lots of compiler errors with GCC7, works with 4.8.5
    # and devs claim it works with 4.7 so I'm assuming 4.7-4.8'll work
    conflicts('%gcc@5:')
    conflicts('%gcc@:4.7.0')

    depends_on('samtools')
    depends_on('jemalloc')
