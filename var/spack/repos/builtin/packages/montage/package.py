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


class Montage(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://montage.ipac.caltech.edu/download/Montage_v5.0.tar.gz"

    version('5.0', sha256='72e034adb77c8a05ac40daf9d1923c66e94faa0b08d3d441256d9058fbc2aa34')

    depends_on('py-setuptools')

    def install(self, spec, prefix):
        make("all")
        make("install")
        install_tree('bin', prefix.bin)
