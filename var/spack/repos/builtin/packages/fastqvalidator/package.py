##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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

    conflicts('%gcc@7:', when='@0.1.1a')

    resource(
        name='libStatGen',
        url='https://github.com/statgen/libStatGen/archive/v1.0.14.tar.gz',
        destination='libStatGen'
    )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make('install')

    def setup_environment(self, spack_env, run_env):
        # Need to make sure self.stage.source_path has a value before setting
        # this variable. Will fail otherwise.
        if self.stage.source_path:
            spack_env.set('LIB_PATH_GENERAL', join_path(self.stage.source_path,
                          'libStatGen', 'libStatGen-1.0.14'))
        spack_env.set('INSTALLDIR', self.prefix.bin)
