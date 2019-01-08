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
import glob


class Tachyon(MakefilePackage):
    """Tachyon parallel ray tracing system."""

    homepage = "http://jedi.ks.uiuc.edu/~johns/raytracer"
    url      = "http://jedi.ks.uiuc.edu/~johns/raytracer/files/0.99b6/tachyon-0.99b6.tar.gz"

    version('0.99b6', sha256='f4dcaf9c76a4f49310f56254390f9611c22e353947a1745a8c623e8bc8119b97')

    def build(self, spec, prefix):
        with working_dir('unix'):
            make('linux-64-thr-ogl')

    def install(self, spec, prefix):
        # Headers
        mkdir(prefix.include)
        headers = glob.iglob('src/*.h')
        for file in headers:
            install(file, prefix.include)
        # Library
        mkdir(prefix.lib)
        install('compile/linux-64-thr-ogl/libtachyon.a', prefix.lib)
        # Executable
        mkdir(prefix.bin)
        install('compile/linux-64-thr-ogl/tachyon', prefix.bin)

