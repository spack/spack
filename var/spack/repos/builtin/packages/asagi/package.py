# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Gilbert Brietzke
# Date: July 2, 2019

from spack import *


class Asagi(CMakePackage):
    """a pArallel Server for Adaptive GeoInformation."""

    homepage = "https://github.com/TUM-I5/ASAGI"
    git = "https://github.com/TUM-I5/ASAGI.git"

    version('f633f96', commit='f633f96931ae00805f599078d5a1a6a830881554',
            submodules=True, preferred=True)

    variant('mpi', default=True, description="enable MPI-parallelization")

    depends_on('mpi', when="+mpi")
    depends_on('netcdf +mpi', when="+mpi")
    depends_on('netcdf ~mpi', when="~mpi")
