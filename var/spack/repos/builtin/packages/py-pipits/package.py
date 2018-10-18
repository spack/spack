# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPipits(PythonPackage):
    """Automated pipeline for analyses of fungal ITS from the Illumina"""

    homepage = "https://github.com/hsgweon/pipits"
    url      = "https://github.com/hsgweon/pipits/archive/1.5.0.tar.gz"

    version('1.5.0', '3f9b52bd7ffbcdb96d7bec150275070a')

    depends_on('python@:2.999', type=('build', 'run'))
    depends_on('py-biom-format', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('java', type=('build', 'run'))
    depends_on('hmmer')
    depends_on('fastx-toolkit')
    depends_on('vsearch')
    depends_on('itsx')
    depends_on('rdp-classifier')

    resource(
        name='UNITE_retrained',
        url='http://sourceforge.net/projects/pipits/files/UNITE_retrained_28.06.2017.tar.gz',
        destination='refdb'
    )

    resource(
        name='uchime_reference_dataset_01.01.2016.fasta',
        url='https://unite.ut.ee/sh_files/uchime_reference_dataset_01.01.2016.zip',
        destination=join_path('refdb', 'uchime_reference_dataset_01.01.2016')
    )

    resource(
        name='warcup_retrained_V2',
        url='https://sourceforge.net/projects/pipits/files/warcup_retrained_V2.tar.gz',
        destination='refdb'
    )

    @run_after('install')
    def install_db(self):
        install_tree(join_path(self.stage.source_path, 'refdb'),
                     self.prefix.refdb)

    def setup_environment(self, spack_env, run_env):
        run_env.set('PIPITS_UNITE_REFERENCE_DATA_CHIMERA', join_path(
                    self.prefix, 'refdb',
                    'uchime_reference_dataset_01.01.2016',
                    'uchime_reference_dataset_01.01.2016.fasta'))
        run_env.set('PIPITS_UNITE_RETRAINED_DIR',
                    self.prefix.refdb.UNITE_retrained)
        run_env.set('PIPITS_WARCUP_RETRAINED_DIR',
                    self.prefix.refdb.warcup_retrained_V2)
        run_env.set('PIPITS_RDP_CLASSIFIER_JAR', join_path(
                    self.spec['rdp-classifier'].prefix.bin,
                    'classifier.jar'))
