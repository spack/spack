# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FalconUnzip(Package):
    """FALCON-Unzip works with FALCON  for full diploid assembly."""

    homepage = "https://github.com/PacificBiosciences/FALCON_unzip/wiki"
    version('2018.31.08-03.06-py2.7-ucs4-beta',
            sha256='bd6a29cc25f39924aad0137da3f1be63dce60f16b0bd044d58728b8407460545',
            url='https://downloads.pacbcloud.com/public/falcon/falcon-2018.03.12-04.00-py2.7-ucs4.tar.gz')

    depends_on('python@2.7.0:2.7.99',  type='run')
    depends_on('mummer',      type='run')
    depends_on('samtools',    type='run')
    depends_on('minimap2',    type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
