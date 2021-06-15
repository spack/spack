# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kineto(CMakePackage):
    """A CPU+GPU Profiling library that provides access to timeline traces
    and hardware performance counters."""

    homepage = "https://github.com/pytorch/kineto"
    git      = "https://github.com/pytorch/kineto.git"

    version('0.1.0', tag='v0.1.0', submodules=True)

    root_cmakelists_dir = 'libkineto'

    depends_on('cmake@3.5:', type='build')
    depends_on('python', type='build')
    depends_on('cuda')
