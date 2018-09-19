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


class Gapbs(MakefilePackage):
    """The GAP Benchmark Suite is intended to help graph processing research by
    standardizing evaluations. Fewer differences between graph processing
    evaluations will make it easier to compare different research efforts and
    quantify improvements. The benchmark not only specifies graph kernels,
    input graphs, and evaluation methodologies, but it also provides an
    optimized baseline implementation (this repo). These baseline
    implementations are representative of state-of-the-art performance, and
    thus new contributions should outperform them to demonstrate an
    improvement."""

    homepage = "http://gap.cs.berkeley.edu/benchmark.html"
    url      = "https://github.com/sbeamer/gapbs/archive/v1.0.tar.gz"

    version('1.0', 'ac2efa793f44e58553449f42b9779f3ff2d47634')

    variant('serial', default=False, description='Version with no parallelism')

    def build(self, spec, prefix):
        cxx_flags = ['-O3', self.compiler.cxx11_flag]

        if '-serial' in spec:
            cxx_flags.append(self.compiler.openmp_flag)

        make('CXX_FLAGS=' + ' '.join(cxx_flags))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for app in ["bc", "bfs", "cc", "converter", "pr", "sssp", "tc"]:
            install(app, prefix.bin)
