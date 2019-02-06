# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ucx(AutotoolsPackage):
    """a communication library implementing high-performance messaging for
    MPI/PGAS frameworks"""

    homepage = "http://www.openucx.org"
    url      = "https://github.com/openucx/ucx/releases/download/v1.3.1/ucx-1.3.1.tar.gz"

    # Current
    version('1.4.0', sha256='99891a98476bcadc6ac4ef9c9f083bc6ffb188a96b3c3bc89c8bbca64de2c76e')

    # Still supported
    version('1.3.1', '443ffdd64dc0e912b672a0ccb37ff666')
    version('1.3.0', '2fdc3028eac3ef3ee1b1b523d170c071')
    version('1.2.2', 'ff3fe65e4ebe78408fc3151a9ce5d286')
    version('1.2.1', '697c2fd7912614fb5a1dadff3bfa485c')

    depends_on('numactl')
    depends_on('rdma-core')
