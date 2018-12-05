# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Muster(CMakePackage):
    """The Muster library provides implementations of sequential and
       parallel K-Medoids clustering algorithms. It is intended as a
       general framework for parallel cluster analysis, particularly
       for performance data analysis on systems with very large
       numbers of processes.
    """
    homepage = "https://github.com/llnl/muster"
    url      = "https://github.com/llnl/muster/archive/v1.0.tar.gz"

    version('1.0.1', 'd709787db7e080447afb6571ac17723c')
    version('1.0',   '2eec6979a4a36d3a65a792d12969be16')

    depends_on('boost')
    depends_on('mpi')
    depends_on('cmake@2.8:', type='build')
