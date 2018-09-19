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


class Fastqvalidator(MakefilePackage):
    """The fastQValidator validates the format of fastq files."""

    homepage = "http://genome.sph.umich.edu/wiki/FastQValidator"
    git      = "https://github.com/statgen/fastQValidator.git"

    version('2017-01-10', commit='6d619a34749e9d33c34ef0d3e0e87324ca77f320')

    resource(
        name='libStatGen',
        git='https://github.com/statgen/libStatGen.git',
        commit='9db9c23e176a6ce6f421a3c21ccadedca892ac0c'
    )

    @property
    def build_targets(self):
        return ['LIB_PATH_GENERAL={0}'.format(
                join_path(self.stage.source_path, 'libStatGen'))]

    @property
    def install_targets(self):
        return [
            'INSTALLDIR={0}'.format(self.prefix.bin),
            'LIB_PATH_GENERAL={0}'.format(
                join_path(self.stage.source_path, 'libStatGen')),
            'install'
        ]
