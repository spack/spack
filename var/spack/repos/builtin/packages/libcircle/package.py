# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcircle(AutotoolsPackage):
    """libcircle provides an efficient distributed queue on a cluster,
       using self-stabilizing work stealing."""

    homepage = "https://github.com/hpc/libcircle"

    version('0.2.1-rc.1', sha256='5747f91cf4417023304dcc92fd07e3617ac712ca1eeb698880979bbca3f54865',
            url='https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz')

    depends_on('mpi')
