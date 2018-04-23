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


class ScanForMatches(Package):
    """scan_for_matches is a utility written in C for locating patterns in DNA
       or protein FASTA files."""

    homepage = "http://blog.theseed.org/servers/2010/07/scan-for-matches.html"
    url      = "http://www.theseed.org/servers/downloads/scan_for_matches.tgz"

    version('2010-7-16', 'f64c9cfb385984ded2a7ad9ad2253d83')

    def install(self, spec, prefix):
        cc = Executable(self.compiler.cc)
        cc('-O', '-o', 'scan_for_matches', 'ggpunit.c', 'scan_for_matches.c')
        mkdirp(prefix.bin)
        install('scan_for_matches', prefix.bin)
