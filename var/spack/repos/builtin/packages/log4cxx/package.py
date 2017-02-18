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


class Log4cxx(AutotoolsPackage):
    """A C++ port of Log4j"""

    homepage = "https://logging.apache.org/log4cxx/latest_stable/"
    url      = "http://mirror.netcologne.de/apache.org/logging/log4cxx/0.10.0/apache-log4cxx-0.10.0.tar.gz"

    version('0.10.0', 'b30ffb8da3665178e68940ff7a61084c')

    depends_on('libxml2')
    depends_on('apr-util')

    build_directory = 'spack-build'

    # patches from https://aur.archlinux.org/packages/log4cxx/
    patch('log4cxx-0.10.0-missing_includes.patch')
    patch('log4cxx-0.10.0-narrowing-fixes-from-upstream.patch')

    def configure_args(self):
        args = ['--disable-static']
        return args
