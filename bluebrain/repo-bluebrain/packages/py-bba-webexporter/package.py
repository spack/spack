# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbaWebexporter(PythonPackage):
    """The web exporter is a suite of tools to facilitate the conversion
    and export of the Blue Brain Atlas pipeline to web-friendly datasets
    to be consumed by the Atlas web app.
    """
    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_web_exporter"
    git      = "git@bbpgitlab.epfl.ch:dke/apps/blue_brain_atlas_web_exporter.git"

    version('0.1.5', tag='v0.1.5')
    version('0.1.4', tag='v0.1.4')
    version('0.1.3', tag='v0.1.3')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pynrrd', type=('build', 'run'))
    depends_on('py-randomaccessbuffer', type=('build', 'run'))
    depends_on('py-rdflib', type=('build', 'run'))
    depends_on('py-pyld', type=('build', 'run'))
    depends_on('py-jsonpath-ng', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
