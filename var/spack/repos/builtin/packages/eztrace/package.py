# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eztrace(AutotoolsPackage):
    """EZTrace is a tool to automatically generate execution traces
       of HPC applications."""

    homepage = "http://eztrace.gforge.inria.fr"
    url      = "https://gitlab.com/eztrace/eztrace/-/archive/eztrace-1.1-10/eztrace-eztrace-1.1-10.tar.gz"
    maintainers = ['trahay']

    version('1.1-10', sha256='97aba8f3b3b71e8e2f7ef47e00c262234e27b9cb4a870c85c525317a83a3f0d4')

    depends_on('mpi')

    # Does not work on Darwin due to MAP_POPULATE
    conflicts('platform=darwin')

    def configure_args(self):
        args = ["--with-mpi={0}".format(self.spec["mpi"].prefix)]
        return args
