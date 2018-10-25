# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
