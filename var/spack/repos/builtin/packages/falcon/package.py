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


class Falcon(PythonPackage):
    """Falcon: a set of tools for fast aligning long reads for consensus
    and assembly.

    The Falcon tool kit is a set of simple code collection which I use
    for studying efficient assembly algorithm for haploid and diploid genomes.
    It has some back-end code implemented in C for speed and some simple
    front-end written in Python for convenience."""

    homepage = "https://github.com/PacificBiosciences/FALCON"
    git      = "https://github.com/PacificBiosciences/FALCON.git"

    version('2017-05-30', commit='86cec6157291679095ea6080b0cde6561eccc041')

    depends_on('py-setuptools', type='run')
    depends_on('py-pypeflow', type='run')
    depends_on('py-networkx@1.7:1.10', type=['build', 'run'])
    depends_on('pacbio-dazz-db', type='run')
    depends_on('pacbio-daligner', type='run')
    depends_on('pacbio-dextractor', type='run')
    depends_on('pacbio-damasker', type='run')
