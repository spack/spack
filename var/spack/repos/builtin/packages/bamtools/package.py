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
import os


class Bamtools(CMakePackage):
    """C++ API & command-line toolkit for working with BAM data."""

    homepage = "https://github.com/pezmaster31/bamtools"
    url      = "https://github.com/pezmaster31/bamtools/archive/v2.4.0.tar.gz"

    version('2.5.1', '98e90632058f85bd5eed6088b3ff912e')
    version('2.5.0', 'dd4185bdba6e3adf2c24b7f93a57233d')
    version('2.4.1', '41cadf513f2744256851accac2bc7baa')
    version('2.4.0', '6139d00c1b1fe88fe15d094d8a74d8b9')
    version('2.3.0', 'd327df4ba037d6eb8beef65d7da75ebc')
    version('2.2.3', '6eccd3e45e4ba12a68daa3298998e76d')

    depends_on('zlib', type='link')

    def cmake_args(self):
        args = []
        rpath = self.rpath
        rpath.append(os.path.join(self.prefix.lib, "bamtools"))
        args.append("-DCMAKE_INSTALL_RPATH=%s" % ':'.join(rpath))
        return args
