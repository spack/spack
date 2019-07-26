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
    version('1.6.0', sha256='360e885dd7f706a19b673035a3477397d100a02eb618371697c7f3ee4e143e2c')
    version('1.5.2', sha256='1a333853069860e86ba69b8d071ccc9871209603790e2b673ec61f8086913fad')
    version('1.5.1', sha256='567119cd80ad2ae6968ecaa4bd1d2a80afadd037ccc988740f668de10d2fdb7e')
    version('1.5.0', sha256='84f6e4fa5740afebb9b1c8bb405c07206e58c56f83120dcfcd8dc89e4b7d7458')
    version('1.4.0', sha256='99891a98476bcadc6ac4ef9c9f083bc6ffb188a96b3c3bc89c8bbca64de2c76e')

    # Still supported
    version('1.3.1', '443ffdd64dc0e912b672a0ccb37ff666')
    version('1.3.0', '2fdc3028eac3ef3ee1b1b523d170c071')
    version('1.2.2', 'ff3fe65e4ebe78408fc3151a9ce5d286')
    version('1.2.1', '697c2fd7912614fb5a1dadff3bfa485c')

    depends_on('numactl')
    depends_on('rdma-core')
