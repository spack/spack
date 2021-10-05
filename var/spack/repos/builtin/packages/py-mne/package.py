# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMne(PythonPackage):
    """MNE python project for MEG and EEG data analysis."""

    homepage = "http://mne.tools/"
    pypi     = "mne/mne-0.23.4.tar.gz"

    version('0.23.4', sha256='ecace5caacf10961ebb74cc5e0ead4d4dbc55fed006eab1e644da144092354e9')
    version('0.18.2', sha256='aa2e72ad3225efdad39b05e67cd5c88dbd5c3fabf5e1705e459347131f114bc6')

    depends_on('python@3.6:', when='@0.23:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-numpy@1.15.4:', when='@0.23:', type=('build', 'run'))
    depends_on('py-numpy@1.11.3:', type=('build', 'run'))
    depends_on('py-scipy@1.1.0:', when='@0.23:', type=('build', 'run'))
    depends_on('py-scipy@0.17.1:', type=('build', 'run'))

    depends_on('py-tqdm', type='test')
