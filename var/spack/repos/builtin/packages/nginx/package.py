##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Nginx(AutotoolsPackage):
    """nginx [engine x] is an HTTP and reverse proxy server, a mail proxy
    server, and a generic TCP/UDP proxy server, originally written by Igor
    Sysoev."""

    homepage = "https://nginx.org/en/"
    url      = "https://nginx.org/download/nginx-1.12.0.tar.gz"

    version('1.13.8', 'df4be9294365782dc1349ca33ce8c4ac')
    version('1.12.0', '995eb0a140455cf0cfc497e5bd7f94b3')

    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-http_ssl_module']
        return args

    def setup_environment(self, spack_env, run_env):
        """Prepend the sbin directory to PATH."""
        run_env.prepend_path('PATH', join_path(self.prefix, 'sbin'))
