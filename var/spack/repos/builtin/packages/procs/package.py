# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Procs(CargoPackage):
    """A modern replacement for ps"""

    homepage  = "https://crates.io/crates/procs"
    crates_io = "procs"
    git       = "https://github.com/dalance/procs.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.10.3', sha256='3c8082ffc492e8a9fbfa2735edd025a7da90ce3b6087d3bc55e98acff5c884d2')
