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


class Ampliconnoise(MakefilePackage):
    """AmpliconNoise is a collection of programs for the removal of noise
       from 454 sequenced PCR amplicons."""

    homepage = "https://code.google.com/archive/p/ampliconnoise/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/ampliconnoise/AmpliconNoiseV1.29.tar.gz"

    version('1.29', 'd6723e6f9cc71d7eb6f1a65ba4643aac')

    depends_on('mpi@2:')
    depends_on('gsl')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.Scripts)
        run_env.set('PYRO_LOOKUP_FILE', join_path(self.prefix, 'Data',
                    'LookUp_E123.dat'))
        run_env.set('SEQ_LOOKUP_FILE', join_path(self.prefix, 'Data',
                    'Tran.dat'))

    def install(self, spec, prefix):
        make('install')
        install_tree('bin', prefix.bin)
        install_tree('Data', prefix.Data)
        install_tree('FastaUnique', prefix.FastaUnique)
        install_tree('FCluster', prefix.FCluster)
        install_tree('NDist', prefix.NDist)
        install_tree('Perseus', prefix.Perseus)
        install_tree('PerseusD', prefix.PerseusD)
        install_tree('PyroDist', prefix.PyroDist)
        install_tree('PyroNoise', prefix.PyroNoise)
        install_tree('PyroNoiseM', prefix.PyroNoiseM)
        install_tree('Scripts', prefix.Scripts)
        install_tree('SeqDist', prefix.SeqDist)
        install_tree('SeqNoise', prefix.SeqNoise)
        install_tree('SplitClusterClust', prefix.SplitClusterClust)
        install_tree('SplitClusterEven', prefix.SplitClusterEven)
        install_tree('Test', prefix.Test)
        install_tree('TestFLX', prefix.TestFLX)
        install_tree('TestTitanium', prefix.TestTitanium)
        install_tree('TestTitaniumFast', prefix.TestTitaniumFast)
