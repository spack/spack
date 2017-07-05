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
import os


class Ampliconnoise(MakefilePackage):
    """AmpliconNoise is a collection of programs for the removal of noise
       from 454 sequenced PCR amplicons."""

    homepage = "https://code.google.com/archive/p/ampliconnoise/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/ampliconnoise/AmpliconNoiseV1.29.tar.gz"

    version('1.29', 'd6723e6f9cc71d7eb6f1a65ba4643aac')

    depends_on('openmpi@2:')
    depends_on('gsl')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', os.path.join(self.prefix, 'Scripts'))
        run_env.set('PYRO_LOOKUP_FILE', os.path.join(self.prefix, 'data', 'LookUp_E123.dat'))
        run_env.set('SEQ_LOOKUP_FILE', os.path.join(self.prefix, 'data', 'Tran.dat'))
