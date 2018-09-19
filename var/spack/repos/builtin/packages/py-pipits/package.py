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
