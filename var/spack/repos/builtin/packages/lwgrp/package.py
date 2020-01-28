# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lwgrp(AutotoolsPackage):
    """Thie light-weight group library provides process group
       representations using O(log N) space and time."""

    homepage = "https://github.com/hpc/lwgrp"
    url      = "https://github.com/hpc/lwgrp/releases/download/v1.0.2/lwgrp-1.0.2.tar.gz"

    version('1.0.2', sha256='c9d4233946e40f01efd0b4644fd9224becec51b9b5f8cbf45f5bac3129b5b536')

    depends_on('mpi')
