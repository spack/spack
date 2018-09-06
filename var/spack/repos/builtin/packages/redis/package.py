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


class Redis(MakefilePackage):
    """Redis is an open source (BSD licensed), in-memory data structure store,
       used as a database, cache and message broker."""

    homepage = "https://redis.io/"
    url      = "http://download.redis.io/releases/redis-4.0.11.tar.gz"

    version('4.0.11', 'a13ccf0f7051f82dc1c979bd94f0b9a9ba039122')
    version('4.0.8',  'f723b327022cef981b4e1d69c37a8db2faeb0622')

    # Redis make file uses a not standard flag to pass the install path
    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
