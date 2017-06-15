##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install abyss
#
# You can edit this file again by typing:
#
#     spack edit abyss
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Abyss(AutotoolsPackage):
    """ABySS is a de novo, parallel, paired-end sequence assembler that is designed for short reads. The single-processor version is useful for assembling genomes up to 100 Mbases in size."""


    homepage = "http://www.bcgsc.ca/platform/bioinfo/software/abyss"
    url      = "http://www.bcgsc.ca/platform/bioinfo/software/abyss/releases/2.0.2/abyss-2.0.2.tar.gz"

    version('2.0.2', '1623f55ad7f4586e80f6e74b1f27c798')

    depends_on('openmpi')
    depends_on('boost')
    depends_on('sparsehash')
    depends_on('sqlite')


    def configure_args(self):
        args = ['--with-mpi=%s' % self.spec['openmpi'].prefix,
                '--with-boost=%s' % self.spec['boost'].prefix,
                '--with-sqlite=%s' % self.spec['sqlite'].prefix] 
        return args

    
