# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fio(AutotoolsPackage):
    """Flexible I/O Tester."""

    homepage = "https://github.com/axboe/fio"
    url      = "https://github.com/axboe/fio/archive/fio-2.19.tar.gz"

    version('2.19', '67125b60210a4daa689a4626fc66c612')

    variant('gui', default=False, description='Enable building of gtk gfio')
    variant('doc', default=False, description='Generate documentation')

    depends_on('gtkplus@2.18:', when='+gui')
    depends_on('cairo',         when='+gui')

    depends_on('py-sphinx', type='build', when='+doc')

    def configure_args(self):
        config_args = []

        if '+gui' in self.spec:
            config_args.append('--enable-gfio')

        return config_args

    @run_after('build')
    def build_docs(self):
        if '+doc' in self.spec:
            make('-C', 'doc', 'html')
            make('-C', 'doc', 'man')
