# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RpcsvcProto(AutotoolsPackage):
    """rpcsvc protocol definitions from glibc."""

    homepage = "https://github.com/thkukuk/rpcsvc-proto"
    url      = "https://github.com/thkukuk/rpcsvc-proto/releases/download/v1.4/rpcsvc-proto-1.4.tar.gz"

    version('1.4', sha256='867e46767812784d8dda6d8d931d6fabb30168abb02d87a2a205be6d5a2934a7')

    depends_on('gettext')

    def configure_args(self):
        return ['LIBS=-lintl']

    @run_before('build')
    def change_makefile(self):
        # Add 'cpp' path for rpcgen
        filter_file('rpcgen/rpcgen',
                    'rpcgen/rpcgen -Y {0}/lib/spack/env'.format(spack.paths.spack_root),
                    'rpcsvc/Makefile')
