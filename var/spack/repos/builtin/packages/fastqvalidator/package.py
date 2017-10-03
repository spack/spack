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


class Fastqvalidator(MakefilePackage):
    """The fastQValidator validates the format of fastq files."""

    homepage = "http://genome.sph.umich.edu/wiki/FastQValidator"
    url      = "https://github.com/statgen/fastQValidator/archive/v0.1.1a.tar.gz"

    version('0.1.1a', '5c5de69527020b72b64f32987409bd12')

    conflicts('%gcc@7:', when='@0.1.1a')  # statgen/fastQValidator#14

    resource(
        name='libStatGen',
        url='https://github.com/statgen/libStatGen/archive/v1.0.14.tar.gz',
        sha256='70a504c5cc4838c6ac96cdd010644454615cc907df4e3794c999baf958fa734b',
    )

    @property
    def build_targets(self):
        return ['LIB_PATH_GENERAL={0}'.format(
                join_path(self.stage.source_path, 'libStatGen-1.0.14'))]

    @property
    def install_targets(self):
        return [
            'INSTALLDIR={0}'.format(self.prefix.bin),
            'LIB_PATH_GENERAL={0}'.format(
                join_path(self.stage.source_path, 'libStatGen-1.0.14')),
            'install'
        ]
