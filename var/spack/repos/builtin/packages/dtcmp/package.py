# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dtcmp(AutotoolsPackage):
    """The Datatype Comparison Library provides comparison operations and
       parallel sort algorithms for MPI applications."""

    homepage = "https://github.com/hpc/dtcmp"
    url      = "https://github.com/hpc/dtcmp/releases/download/v1.0.3/dtcmp-1.0.3.tar.gz"

    version('1.1.0', 'af5c73f7d3a9afd90a22d0df85471d2f')
    version('1.0.3', 'cdd8ccf71e8ff67de2558594a7fcd317')

    depends_on('mpi')
    depends_on('lwgrp')

    def configure_args(self):
        return ["--with-lwgrp=" + self.spec['lwgrp'].prefix]
