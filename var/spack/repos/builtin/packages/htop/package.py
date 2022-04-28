# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/htop-dev/htop"
    url      = "https://github.com/htop-dev/htop/archive/refs/tags/3.0.5.tar.gz"
    list_url = "https://github.com/htop-dev/htop/releases"
    list_depth = 1

    version('3.0.5', sha256='4c2629bd50895bd24082ba2f81f8c972348aa2298cc6edc6a21a7fa18b73990c')

    variant('unicode', default=True,
            description='enable Unicode support dependency')
    variant('hwloc', default=False,
            description='Enable hwloc support for CPU affinity')
    variant('static', default=False, description='Build a static htop binary')
    variant('debug', default=False,
            description='Enable asserts and internal sanity checks')

    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('hwloc', when='+hwloc')
    depends_on('ncurses', when='+unicode')
    depends_on('python+pythoncmd', type='build')

    conflicts('+static', when='+hwloc')

    def configure_args(self):
        args = ['--enable-shared']

        if self.spec.satisfies('+hwloc'):
            args.append('--enable-hwloc')
        if self.spec.satisfies('+static'):
            args.append('--enable-static')
        if self.spec.satisfies('+debug'):
            args.append('--enable-debug')

        return args
