# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Knem(AutotoolsPackage):
    """KNEM is a Linux kernel module enabling high-performance intra-node MPI
    communication for large messages."""

    homepage = "http://knem.gforge.inria.fr"
    url = "http://gforge.inria.fr/frs/download.php/37186/knem-1.1.3.tar.gz"
    list_url = "http://knem.gforge.inria.fr/download"

    maintainers = ['skosukhin']

    version('1.1.3', sha256='50d3c4a20c140108b8ce47aaafd0ade0927d6f507e1b5cc690dd6bddeef30f60')

    variant('hwloc', default=True,
            description='Enable hwloc in the user-space tools')

    depends_on('hwloc', when='+hwloc')
    depends_on('pkgconfig', type='build', when='+hwloc')

    # The support for hwloc was added in 0.9.1:
    conflicts('+hwloc', when='@:0.9.0')

    # Ideally, we should list all non-Linux-based platforms here:
    conflicts('platform=darwin')

    # All compilers except for gcc are in conflict:
    for __compiler in spack.compilers.supported_compilers():
        if __compiler != 'gcc':
            conflicts('%{0}'.format(__compiler),
                      msg='Linux kernel module must be compiled with gcc')

    @run_before('build')
    def override_kernel_compiler(self):
        # Override the compiler for kernel module source files. We need
        # this additional argument for all installation phases.
        make.add_default_arg('CC={0}'.format(spack_cc))

    def configure_args(self):
        return self.enable_or_disable('hwloc')
