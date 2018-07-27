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


class Halc(MakefilePackage):
    """HALC is software that makes error correction for long reads with
     high throughput."""

    homepage = "https://github.com/lanl001/halc"
    url      = "https://github.com/lanl001/halc/archive/v1.1.tar.gz"

    version('1.1', '4b289b366f6a5400ca481993aa68dd9c')

    depends_on('blasr', type='run')
    depends_on('lordec', type='run')
    depends_on('dos2unix', type='build')
    depends_on('python', type='run')

    parallel = False

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install('runHALC.py', prefix.bin)
        dos2unix = which('dos2unix')
        dos2unix(join_path(self.prefix.bin, 'runHALC.py'))
