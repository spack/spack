# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbaDatafetch(PythonPackage):
    """This module is a (Python) CLI in charge of fetching datasets from
    Nexus, one file (or payload) at the time. It can fetch payloads and
    save them as JSON files or it can fetch binaries (distributions)
    linked to resources.
    """
    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_data_fetch"
    git      = "git@bbpgitlab.epfl.ch:dke/apps/blue_brain_atlas_data_fetch.git"

    version('0.1.0', tag='v0.1.0')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-nexus-sdk', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pynrrd', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
