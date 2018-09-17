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


class Davix(CMakePackage):
    """High-performance file management over WebDAV/HTTP."""

    homepage = "https://dmc.web.cern.ch/projects/davix"
    url      = "http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/davix/0.6.7/davix-0.6.7.tar.gz"
    list_url = "http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/davix/"
    list_depth = 1

    version('0.6.7', 'f811647d924a6dc5852c92110359ed91')

    depends_on('pkgconfig', type='build')
    depends_on('libxml2')
    depends_on('libuuid')
    depends_on('openssl')

    patch('davix-0.6.7-uuid.patch', when="@0.6.7")
