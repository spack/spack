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


class Bamutil(MakefilePackage):
    """bamUtil is a repository that contains several programs
       that perform operations on SAM/BAM files. All of these programs
       are built into a single executable, bam.
    """

    homepage = "http://genome.sph.umich.edu/wiki/BamUtil"
    url      = "http://genome.sph.umich.edu/w/images/7/70/BamUtilLibStatGen.1.0.13.tgz"

    version('1.0.13', '08b7d0bb1d60be104a11f0e54ddf4a79')

    depends_on('zlib', type=('build', 'link'))

    # Looks like this will be fixed in 1.0.14.
    # https://github.com/statgen/libStatGen/issues/9
    patch('libstatgen-issue-9.patch', when='@1.0.13:')

    parallel = False

    @property
    def install_targets(self):
        return ['install', 'INSTALLDIR={0}'.format(self.prefix.bin)]
