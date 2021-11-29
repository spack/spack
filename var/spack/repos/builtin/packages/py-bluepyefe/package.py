##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBluepyefe(PythonPackage):
    """ Blue Brain Python E-feature extraction"""

    homepage = "https://github.com/BlueBrain/BluePyEfe"
    url = "https://pypi.io/packages/source/b/bluepyefe/bluepyefe-0.3.13.tar.gz"
    git = "https://github.com/BlueBrain/BluePyEfe.git"

    version('BPE2', branch='BPE2')

    version('0.3.13', sha256='e274780a34e802eae9ba146782f0b9b088734b38bdc2d6da936d79369306b726')

    depends_on('py-setuptools', type='build')
    depends_on('py-efel', type=('build', 'run'))
    depends_on('py-igor', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-neo', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-sh', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
