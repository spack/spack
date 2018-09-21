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


class Rclone(Package):
    """Rclone is a command line program to sync files and directories
       to and from various cloud storage providers"""

    homepage = "http://rclone.org"
    url      = "https://github.com/ncw/rclone/releases/download/v1.43/rclone-v1.43.tar.gz"

    version('1.43', sha256='d30527b00cecb4e5e7188dddb78e5cec62d67cf2422dab82190db58512b5a4e3')

    depends_on("go", type='build')

    def install(self, spec, prefix):
        go('build')
        mkdirp(prefix.bin)
        install('rclone', prefix.bin)
