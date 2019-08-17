# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fseq(Package):
    """F-Seq: A Feature Density Estimator for High-Throughput Sequence Tags"""

    homepage = "http://fureylab.web.unc.edu/software/fseq/"
    url      = "http://fureylab.med.unc.edu/fseq/fseq_1.84.tgz"

    version('1.84', 'f9124ad0f45c60f3a7eb74dde8c945b9')

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install('mapviewToBed.pl', prefix.bin)
