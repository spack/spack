# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenpmdViewer(PythonPackage):
    """Python visualization tools for openPMD files"""

    homepage = "https://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-viewer/archive/refs/tags/1.2.0.tar.gz"
    git      = "https://github.com/openPMD/openPMD-viewer.git"

    maintainers = ['RemiLehe', 'ax3l']

    version('1.2.0', sha256='a27f8ac522c4c76fd774095e156a8b280c9211128f50aa07f16ac70d8222384d')

    variant('jupyter', default=False,
            description='Enable Jupyter Widget GUI')
    variant('numba', default=False,
            description='Enable accelerated depositions for histograms')

    depends_on('openpmd-api +python -mpi', type=('build', 'run'))

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-h5py@2.8.0:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-wget', type=('build', 'run'))  # Tutorials

    with when('+jupyter'):
        # missing in Spack:
        #depends_on('py-ipympl', type=('build', 'run'))
        depends_on('py-ipywidgets', type=('build', 'run'))
        depends_on('py-jupyter', type=('build', 'run'))
        depends_on('py-tqdm +notebook', type=('build', 'run'))

    with when('+numba'):
        depends_on('py-numba', type=('build', 'run'))
