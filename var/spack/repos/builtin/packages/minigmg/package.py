##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import glob


class Minigmg(Package):
    """miniGMG is a compact benchmark for understanding the performance
    challenges associated with geometric multigrid solvers
    found in applications built from AMR MG frameworks
    like CHOMBO or BoxLib when running
    on modern multi- and manycore-based supercomputers.
    It includes both productive reference examples as well as
    highly-optimized implementations for CPUs and GPUs.
    It is sufficiently general that it has been used to evaluate
    a broad range of research topics including PGAS programming models
    and algorithmic tradeoffs inherit in multigrid. miniGMG was developed
    under the CACHE Joint Math-CS Institute.

    Note, miniGMG code has been supersceded by HPGMG. """

    homepage = "http://crd.lbl.gov/departments/computer-science/PAR/research/previous-projects/miniGMG/"
    url      = "http://crd.lbl.gov/assets/Uploads/FTG/Projects/miniGMG/miniGMG.tar.gz"

    version('master', '975a2a118403fc0024b5e04cef280e95')

    depends_on('mpi')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spec['mpi'].mpicc)
        cc('-O3', self.compiler.openmp_flag, 'miniGMG.c',
            'mg.c', 'box.c', 'solver.c', 'operators.ompif.c', 'timer.x86.c',
            '-D__MPI', '-D__COLLABORATIVE_THREADING=6',
            '-D__TEST_MG_CONVERGENCE', '-D__PRINT_NORM', '-D__USE_BICGSTAB',
            '-o', 'run.miniGMG', '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('run.miniGMG', prefix.bin)
        mkdir(prefix.jobs)
        files = glob.glob('job*')
        for f in files:
            install(f, prefix.jobs)
