# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os import unlink
from glob import glob


class PyDpGpCluster(PythonPackage):
    """DP_GP_cluster clusters genes by expression over a time course using a
       Dirichlet process Gaussian process model."""

    homepage = "https://github.com/PrincetonUniversity/DP_GP_cluster"
    git      = "https://github.com/PrincetonUniversity/DP_GP_cluster.git"

    version('master', branch='master')

    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-gpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@0.14:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    @run_before('build')
    def remove_cython_output(self):
        for f in glob('DP_GP/*.c'):
            unlink(f)
