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


class Sz(AutotoolsPackage):
    """Error-bounded Lossy Compressor for HPC Data."""

    homepage = "https://collab.cels.anl.gov/display/ESR/SZ"
    url      = "https://github.com/disheng222/SZ/archive/v1.4.13.5.tar.gz"

    version('develop', git='https://github.com/disheng222/SZ.git',
            branch='master')
    version('1.4.13.5', 'a2f6147c3c74d74c938dd17d914a4cb8')
    version('1.4.13.4', '1c47170a9eebeadbf0f7e9b675d68d76')
    version('1.4.12.3', '5f51be8530cdfa5280febb410ac6dd94')
    version('1.4.11.0', '10dee28b3503821579ce35a50e352cc6')
    version('1.4.10.0', '82e23dc5a51bcce1f70ba7e3b68a5965')
    version('1.4.9.2',  '028ce90165b7a4c4051d4c0189f193c0')

    variant('fortran', default=False,
            description='Enable fortran compilation')

    def configure_args(self):
        args = []
        if '+fortran' in self.spec:
            args += ['--enable-fortran']
        else:
            args += ['--disable-fortran']
        return args
