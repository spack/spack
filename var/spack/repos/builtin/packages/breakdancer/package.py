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


class Breakdancer(CMakePackage):
    """BreakDancer-1.3.6, released under GPLv3, is a Cpp package that provides
    genome-wide detection of structural variants from next generation
    paired-end sequencing reads. It includes two complementary programs.
    BreakDancerMax predicts five types of structural variants: insertions,
    deletions, inversions, inter- and intra-chromosomal translocations from
    next-generation short paired-end sequencing reads using read pairs that are
    mapped with unexpected separation distances or orientation.
    BreakDancerMini focuses on detecting small indels (usually between 10bp and
    100bp) using normally mapped read pairs.."""

    homepage = "http://gmt.genome.wustl.edu/packages/breakdancer"
    git      = "https://github.com/genome/breakdancer.git"

    version('master', submodules='true')

    depends_on('zlib')

    parallel = False
