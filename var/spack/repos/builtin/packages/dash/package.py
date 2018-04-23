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


class Dash(AutotoolsPackage):
    """The Debian Almquist Shell."""

    homepage = "https://git.kernel.org/pub/scm/utils/dash/dash.git"
    url      = "https://git.kernel.org/pub/scm/utils/dash/dash.git/snapshot/dash-0.5.9.1.tar.gz"
    list_url = homepage

    version('0.5.9.1', '0d800da0b8ddbefa1468978d314b7d09')

    depends_on('libedit', type='link')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def configure_args(self):
        # Compile with libedit support
        # This allows the use of arrow keys at the command line
        # See https://askubuntu.com/questions/704688
        return ['--with-libedit']
