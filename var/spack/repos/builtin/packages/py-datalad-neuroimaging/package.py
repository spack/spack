# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDataladNeuroimaging(PythonPackage):
    """DataLad extension package for neuro/medical imaging"""

    homepage = "https://github.com/datalad/datalad-neuroimaging"
    pypi     = "datalad_neuroimaging/datalad_neuroimaging-0.3.1.tar.gz"

    version('0.3.1', sha256='aaf7a3d10e8e7df1d8dee09e485bbe26787f496fb2302ed7ddea55a470a0f96e')

    depends_on('py-setuptools', type='build')
    depends_on('py-datalad@0.12:', type=('build', 'run'))
    depends_on('py-pydicom', type=('build', 'run'))
    depends_on('py-pybids@0.9.2:', type=('build', 'run'))
    depends_on('py-nibabel', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('git-annex', type='run')
