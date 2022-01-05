# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDataIntegrityCheck(PythonPackage):
    """This module contains CLIs for performing verifications of various
    atlas pipeline files integrity.
    """
    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_data_integrity_check.git"
    git      = "git@bbpgitlab.epfl.ch:dke/apps/blue_brain_atlas_data_integrity_check.git"

    version('0.1.0', tag='v0.1.0')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-h5py@3.1.0:', type=('build', 'run'))
    depends_on('py-numpy@1.19.0:', type=('build', 'run'))
    depends_on('py-pynrrd@0.4.0:', type=('build', 'run'))
    depends_on('py-pytest@4.3.0:', type='test')
    depends_on('py-pytest-cov@2.8.1:', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
