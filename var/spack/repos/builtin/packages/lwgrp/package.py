# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lwgrp(AutotoolsPackage):
    """Thie light-weight group library provides process group
       representations using O(log N) space and time."""

    homepage = "https://github.com/hpc/lwgrp"
    url      = "https://github.com/hpc/lwgrp/releases/download/v1.0.2/lwgrp-1.0.2.tar.gz"

    version('1.0.2', 'ab7ba3bdd8534a651da5076f47f27d8a')

    depends_on('mpi')
