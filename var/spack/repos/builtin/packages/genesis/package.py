# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genesis(AutotoolsPackage):
    """GENESIS (GENeralized-Ensemble SImulation System) is molecular dynamics
    and modeling software for bimolecular systems such as proteins, lipids,
    glycans, and their complexes. GENESIS is open source software distributed
    under the GPLv2 license."""

    homepage = "https://www.r-ccs.riken.jp/labs/cbrt/"

    version('1.3.0', sha256='99aae81c1dc33cae06a86d4e808e73fc6829d5199bfed88863cbd7019f7e754b',
            url="https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2018/06/genesis-1.3.0.tar.bz2")

    depends_on('mpi@2:')
    depends_on('blas')
    depends_on('lapack')
#    depends_on('scalapack')

    def configure_args(self):
        args = []
        return args
