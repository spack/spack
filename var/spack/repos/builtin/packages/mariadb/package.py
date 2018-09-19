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


class Mariadb(CMakePackage):
    """MariaDB turns data into structured information in a wide array of
    applications, ranging from banking to websites. It is an enhanced, drop-in
    replacement for MySQL. MariaDB is used because it is fast, scalable and
    robust, with a rich ecosystem of storage engines, plugins and many other
    tools make it very versatile for a wide variety of use cases."""

    homepage = "https://mariadb.org/about/"
    url      = "http://ftp.hosteurope.de/mirror/archive.mariadb.org/mariadb-10.2.8/source/mariadb-10.2.8.tar.gz"

    version('10.2.8', 'f93cbd5bfde3c0d082994764ff7db580')
    version('10.1.23', '1a7392cc05c7c249acd4495022719ca8')
    version('5.5.56', '8bc7772fea3e11b0bc1a09d2278e2e32')
    version('10.1.14', '294925531e0fd2f0461e3894496a5adc')
    version('5.5.49', '67b5a499a5f158b2a586e6e3bfb4f304')

    variant('nonblocking', default=True, description='Allow non blocking '
            'operations in the mariadb client library.')

    depends_on('boost')
    depends_on('cmake@2.6:', type='build')
    depends_on('jemalloc')
    depends_on('libaio')
    depends_on('libedit')
    depends_on('libevent', when='+nonblocking')
    depends_on('ncurses')
    depends_on('zlib')
