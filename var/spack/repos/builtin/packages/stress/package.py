# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stress(AutotoolsPackage):
    """stress is a deliberately simple workload generator for POSIX systems.
    It imposes a configurable amount of CPU, memory, I/O, and disk stress on
    the system. It is written in C, and is free software licensed under the
    GPLv2."""

    homepage = "https://people.seas.harvard.edu/~apw/stress/"
    url      = "https://people.seas.harvard.edu/~apw/stress/stress-1.0.4.tar.gz"

    version('1.0.4', '890a4236dd1656792f3ef9a190cf99ef')
