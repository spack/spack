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

class Samtools(Package):
    """SAM Tools provide various utilities for manipulating alignments in the SAM format, 
       including sorting, merging, indexing and generating
       alignments in a per-position format"""

    homepage = "www.htslib.org"
    version('1.2','988ec4c3058a6ceda36503eebecd4122',url = "https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2")

    depends_on("zlib")
    depends_on("mpc")
    parallel=False
    patch("samtools1.2.patch",level=0)

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")

