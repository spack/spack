##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
    url      = "https://github.com/disheng222/SZ/archive/v1.4.9.2.tar.gz"

    version('develop', git='https://github.com/disheng222/SZ.git',
            branch='master')
    version('1.4.9.2', '028ce90165b7a4c4051d4c0189f193c0')

    variant('fortran', default=False,
            description='Enable fortran compilation')

    def configure_args(self):
        args = []
        if '+fortran' in self.spec:
            args += ['--enable-fortran']
        else:
            args += ['--disable-fortran']
        return args
