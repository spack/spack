# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sparta(Package):
    """small RNA-PARE Target Analyzer (sPARTA) is a tool which utilizes
       high-throughput sequencing to profile genome-wide cleavage
       products."""

    homepage = "https://github.com/atulkakrana/sPARTA.github"
    url      = "https://github.com/atulkakrana/sPARTA/archive/1.25.tar.gz"

    version('1.25', '50fda66bf860f63ae8aef5e8fb997a75')

    depends_on('bowtie2')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('sPARTA.py', prefix.bin)
        install('revFernoMap.py', prefix.bin)
