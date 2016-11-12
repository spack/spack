##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class PyTornado(Package):
    """Tornado is a Python web framework and asynchronous networking
    library."""
    homepage = "https://github.com/tornadoweb/tornado"
    # base https://pypi.python.org/pypi/tornado/
    url      = "https://github.com/tornadoweb/tornado/archive/v4.4.0.tar.gz"

    version('4.4.0', 'c28675e944f364ee96dda3a8d2527a87ed28cfa3')
    
    variant('futures', default=True, description="recommended thread pool and for tornado.netutil.ThreadedResolver")
    variant('monotonic', default=True, description="enable support for a monotonic clock")
    variant('curl', default=True, description="for tornado.curl_httpclient")
    variant('twisted', default=True, description="for tornado.platform.twisted")

    extends('python')
    depends_on('py-setuptools', type='build')
    depends_on('py-certifi')
    depends_on('py-backports-abc', when='^python@:2')
    depends_on('py-singledispatch', when='^python@:2')
    depends_on('py-futures', when='+futures^python@:2')
    depends_on('py-monotonic', when='+monotonic^python@:2')
    depends_on('py-pycurl', when='+curl')
    depends_on('py-twisted', when='+twisted')

    def install(self, spec, prefix):
        setup_py('build')
        setup_py('install', '--prefix={0}'.format(prefix))
