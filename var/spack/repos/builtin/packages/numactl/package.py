# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Numactl(AutotoolsPackage):
    """NUMA support for Linux"""

    homepage = "http://oss.sgi.com/projects/libnuma/"
    url      = "https://github.com/numactl/numactl/releases/download/v2.0.14/numactl-2.0.14.tar.gz"

    version('2.0.14', sha256='826bd148c1b6231e1284e42a4db510207747484b112aee25ed6b1078756bcff6')
    version('2.0.12', sha256='55bbda363f5b32abd057b6fbb4551dd71323f5dbb66335ba758ba93de2ada729')
    version('2.0.11', sha256='450c091235f891ee874a8651b179c30f57a1391ca5c4673354740ba65e527861')

    patch('numactl-2.0.11-sysmacros.patch', when="@2.0.11")
    # https://github.com/numactl/numactl/issues/94
    patch('numactl-2.0.14-symver.patch', when="@2.0.14")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc'):
            filter_file('-ffast-math -funroll-loops', '', 'Makefile.am')
            filter_file('-std=gnu99', '-c99', 'Makefile.am')

        # Avoid undefined reference errors
        if self.spec.satisfies('@2.0.14 %nvhpc'):
            filter_file('numa_sched_setaffinity_v1_int',
                        'numa_sched_setaffinity_v1', 'libnuma.c')
            filter_file('numa_sched_setaffinity_v2_int',
                        'numa_sched_setaffinity_v2', 'libnuma.c')
            filter_file('numa_sched_getaffinity_v2_int',
                        'numa_sched_getaffinity_v2', 'libnuma.c')
