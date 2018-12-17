# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nginx(AutotoolsPackage):
    """nginx [engine x] is an HTTP and reverse proxy server, a mail proxy
    server, and a generic TCP/UDP proxy server, originally written by Igor
    Sysoev."""

    homepage = "https://nginx.org/en/"
    url      = "https://nginx.org/download/nginx-1.12.0.tar.gz"

    version('1.15.6', 'a3d8c67c2035808c7c0d475fffe263db8c353b11521aa7ade468b780ed826cc6')
    version('1.13.8', 'df4be9294365782dc1349ca33ce8c4ac')
    version('1.12.0', '995eb0a140455cf0cfc497e5bd7f94b3')

    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')

    conflicts('%gcc@8:', when='@:1.14')

    def configure_args(self):
        args = ['--with-http_ssl_module']
        return args

    def setup_environment(self, spack_env, run_env):
        """Prepend the sbin directory to PATH."""
        run_env.prepend_path('PATH', join_path(self.prefix, 'sbin'))
