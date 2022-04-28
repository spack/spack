# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/htop-dev/htop"
    maintainers = ['sethrj']
    url      = "https://github.com/htop-dev/htop/archive/refs/tags/3.1.1.tar.gz"
    list_url = "https://github.com/htop-dev/htop/releases"
    list_depth = 1

    version('3.1.1', sha256='b52280ad05a535ec632fbcd47e8e2c40a9376a9ddbd7caa00b38b9d6bb87ced6')
    version('3.0.5', sha256='4c2629bd50895bd24082ba2f81f8c972348aa2298cc6edc6a21a7fa18b73990c')
    version('2.2.0', sha256='d9d6826f10ce3887950d709b53ee1d8c1849a70fa38e91d5896ad8cbc6ba3c57', url='https://hisham.hm/htop/releases/2.2.0/htop-2.2.0.tar.gz')
    version('2.0.2', sha256='179be9dccb80cee0c5e1a1f58c8f72ce7b2328ede30fb71dcdf336539be2f487', url='https://hisham.hm/htop/releases/2.0.2/htop-2.0.2.tar.gz')
    
    variant('unicode', default=True,
            description='enable Unicode support dependency')
    variant('hwloc', default=False,
            description='Enable hwloc support for CPU affinity')
    variant('static', default=False, 
            description='Build a static htop binary')
    variant('debug', default=False,
            description='Enable asserts and internal sanity checks')

    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('hwloc', when='+hwloc')
    depends_on('ncurses', when='+unicode')
    depends_on('ncurses@6:', when='@3:')
    
    depends_on('ncurses')

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
