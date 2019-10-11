# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nextflow(Package):
    """Data-driven computational pipelines"""

    homepage = "http://www.nextflow.io"
    url = "https://github.com/nextflow-io/nextflow/releases/download/v0.24.1/nextflow"

    version('0.25.6', '29d739b6caf8ceb5aa9997310ee8d0e7', expand=False)
    version('0.24.1', '80ec8c4fe8e766e0bdd1371a50410d1d', expand=False)
    version('0.23.3', '71fb69275b6788af1c6f1165f40d362e', expand=False)
    version('0.21.0', '38e5e335cb33f05ba358e1f883c8386c', expand=False)
    version('0.20.1', '0e4e0e3eca1c2c97f9b4bffd944b923a', expand=False)
    version('0.17.3', '5df00105fb1ce6fd0ba019ae735d9617', expand=False)

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("nextflow", join_path(prefix.bin, "nextflow"))
        set_executable(join_path(prefix.bin, "nextflow"))
