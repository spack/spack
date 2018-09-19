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


class Strelka(CMakePackage):
    """Somatic and germline small variant caller for mapped sequencing
       data."""

    homepage = "https://github.com/Illumina/strelka"
    url      = "https://github.com/Illumina/strelka/releases/download/v2.8.2/strelka-2.8.2.release_src.tar.bz2"

    version('2.8.2', 'c48753997fcf2e4edac4e9854495721e')

    depends_on('python@2.4:')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('cmake@2.8.5:')
    depends_on('boost@1.56.0:')

    @run_before('install')
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
           can fix up the path to the python binary.
        """

        match = '^#!/usr/bin/env python'
        python = self.spec['python'].command
        substitute = "#!{p}".format(p=python)
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        with working_dir('src'):
            files = [
                'config/validate/validateJsonModelFromSchema.py',
                'srcqc/run_cppcheck.py',
                'python/libexec/cat.py',
                'python/libexec/sortVcf.py',
                'python/libexec/extractSmallIndelCandidates.py',
                'python/libexec/configureStrelkaNoiseWorkflow.py',
                'python/libexec/configureSequenceErrorCountsWorkflow.py',
                'python/libexec/vcfCmdlineSwapper.py',
                'python/libexec/mergeChromDepth.py',
                'python/scoringModelTraining/germline/bin/evs_learn.py',
                'python/scoringModelTraining/germline/bin/parseAnnotatedTrainingVcf.py',  # noqa: E501
                'python/scoringModelTraining/germline/bin/filterTrainingVcf.py',  # noqa: E501
                'python/scoringModelTraining/germline/bin/evs_exportmodel.py',
                'python/scoringModelTraining/germline/bin/evs_qq.py',
                'python/scoringModelTraining/germline/bin/evs_pr.py',
                'python/scoringModelTraining/germline/bin/evs_evaluate.py',
                'python/scoringModelTraining/somatic/bin/evs_random_sample_tpfp.py',  # noqa: E501
                'python/scoringModelTraining/somatic/bin/evs_learn.py',
                'python/scoringModelTraining/somatic/bin/evs_random_split_csv.py',  # noqa: E501
                'python/scoringModelTraining/somatic/bin/vcf_to_feature_csv.py',  # noqa: E501
                'python/scoringModelTraining/somatic/bin/calc_features.py',
                'python/scoringModelTraining/somatic/bin/evs_exportmodel.py',
                'python/scoringModelTraining/somatic/bin/evs_pr.py',
                'python/scoringModelTraining/somatic/bin/evs_evaluate.py',
                'python/bin/configureStrelkaGermlineWorkflow.py',
                'python/bin/configureStrelkaSomaticWorkflow.py',
            ]
            filter_file(match, substitute, *files, **kwargs)

        with working_dir('spack-build/redist'):
            files = [
                'pyflow-1.1.18/src/pyflow.py',
            ]
            filter_file(match, substitute, *files, **kwargs)
