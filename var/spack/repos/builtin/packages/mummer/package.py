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


class Mummer(Package):
    """MUMmer is a system for rapidly aligning entire genomes."""

    homepage = "http://mummer.sourceforge.net/"
    url      = "https://sourceforge.net/projects/mummer/files/mummer/3.23/MUMmer3.23.tar.gz/download"

    version('3.23', 'f2422b3d2638dba4baedb71b1acdffa2')

    depends_on('gnuplot')

    def install(self, spec, prefix):
        if self.run_tests:
            make('check')
        make('install')
        mkdirp(prefix.bin)

        bins = ["show-tiling", "show-snps", "show-coords", "show-aligns", 
                "show-diff", "delta-filter", "combineMUMs", "mummer", 
                "repeat-match", "annotate", "mgaps", "gaps", "dnadiff", 
                "nucmer2xfig", "run-mummer3", "mummerplot", "promer", 
                "run-mummer1", "nucmer", "mapview", "exact-tandems"]
        aux_bins = ["aux_bin/postnuc", "aux_bin/postpro",
                    "aux_bin/prenuc", "aux_bin/prepro"]
                  
        for b in bins:
            install(b, join_path(prefix.bin, b))
        for b in aux_bins:
            install(b, join_path(prefix.bin, b[8:]))
