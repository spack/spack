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


class Fyba(AutotoolsPackage):
    """OpenFYBA is the source code release of the FYBA library, distributed
    by the National Mapping Authority of Norway (Statens kartverk) to read
    and write files in the National geodata standard format SOSI."""

    homepage = "https://github.com/kartverket/fyba"
    url      = "https://github.com/kartverket/fyba/archive/4.1.1.tar.gz"

    version('4.1.1', 'ab687582efdef26593796271529a10cb')

    # configure: error: cannot find install-sh or install.sh
    force_autoreconf = True

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # error: macro "min" passed 3 arguments, but takes just 2
    # https://github.com/kartverket/fyba/issues/21
    patch('gcc-6.patch')

    # fatal error: 'sys/vfs.h' file not found
    # https://github.com/kartverket/fyba/issues/12
    patch('vfs-mount-darwin.patch', when='platform=darwin')
