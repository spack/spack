# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *


class Prrte(AutotoolsPackage):
    """PRRTE is the Reference RunTime Environment implementation for PMIx.
       It is capable of operating within a host SMS. The reference RTE
       therefore provides an easy way of exploring PMIx capabilities and
       testing PMIx-based applications outside of a PMIx-enabled
       environment."""

    homepage = "https://pmix.org"
    url      = "https://github.com/pmix/prrte/archive/dev.tar.gz"
    git      = "https://github.com/pmix/prrte.git"

    version('develop', branch='master')

    depends_on('pmix')
    depends_on('libevent')
    depends_on('hwloc')
    depends_on('perl', type=('build'))
    depends_on('m4', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('libtool', type=('build'))
    depends_on('flex', type=('build'))

    def autoreconf(self, spec, prefix):
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        with working_dir(self.configure_directory):
            perl = spec['perl'].command
            perl('autogen.pl')

    def configure_args(self):

        spec = self.spec
        config_args = [
            '--enable-shared',
            '--enable-static'
        ]

        # libevent
        config_args.append(
            '--with-libev={0}'.format(spec['libevent'].prefix))
        # hwloc
        config_args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))
        # pmix
        config_args.append('--with-pmix={0}'.format(spec['pmix'].prefix))

        return config_args
