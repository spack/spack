# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package_defs import *


class FluxPmix(AutotoolsPackage):
    """ A flux shell plugin to bootstrap openmpi v5+ """

    homepage = "https://github.com/flux-framework/flux-pmix"
    url      = "https://github.com/flux-framework/flux-pmix/releases/download/v0.1.0/flux-pmix-0.1.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-pmix.git"

    maintainers = ['grondo']

    version('main', branch='main')
    version('0.2.0', sha256='d09f1fe6ffe54f83be4677e1e727640521d8110090515d94013eba0f58216934')

    depends_on('flux-core@0.30.0:')
    depends_on('pmix@v4.1.0:')
    depends_on('openmpi')

    depends_on('pkgconfig', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    def autoreconf(self, spec, prefix):
        if not os.path.exists('configure'):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

    @run_after('install')
    def add_pluginpath(self):
        rcfile = join_path(self.prefix.etc,
                           'flux/shell/lua.d/mpi/openmpi@5.lua')
        filter_file(r'pmix/pmix.so',
                    join_path(self.prefix.lib,
                              "flux/shell/plugins/pmix/pmix.so"), rcfile)

    def setup_run_environment(self, env):
        env.prepend_path('FLUX_SHELL_RC_PATH',
                         join_path(self.prefix, 'etc/flux/shell/lua.d'))
