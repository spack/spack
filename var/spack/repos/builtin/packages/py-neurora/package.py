# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyNeurora(PythonPackage):
    """A Python Toolbox for Multimodal Neural Data Representation Analysis."""

    homepage = "https://github.com/ZitongLu1996/NeuroRA"
    pypi     = "neurora/neurora-1.1.5.16.tar.gz"

    version('1.1.6.1', sha256='97b2d1287f273a8db11dcaa623fc906b47ee7c4459e264a42b131e6a4f332916')
    version('1.1.5.16', sha256='5ae296a5baf658b67e9754a172f5fb321c2077007455f93db6bb2aaeb3e23cd7')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@1.6.2:', type=('build', 'run'))
    depends_on('py-mne', type=('build', 'run'))
    depends_on('py-nibabel', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-nilearn', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
