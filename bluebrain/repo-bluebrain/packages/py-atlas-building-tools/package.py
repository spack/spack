# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasBuildingTools(PythonPackage):
    """BBP Python tools to build brain region atlases."""
    homepage = "https://bbpgitlab.epfl.ch/nse/atlas-building-tools"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/atlas-building-tools.git"

    version('develop', branch='main')
    version('0.1.9', tag='atlas-building-tools-v0.1.9')

    depends_on('py-atlas-densities@0.1.3:', type=('build', 'run'))
    depends_on('py-atlas-direction-vectors@0.1.1:', type=('build', 'run'))
    depends_on('py-atlas-placement-hints@0.1.1:', type=('build', 'run'))
    depends_on('py-atlas-splitter@0.1.1:', type=('build', 'run'))
    depends_on('py-cgal-pybind@0.1.4:', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-pillow@7.1.2:', type=('build', 'run'))
    depends_on('py-poisson-recon-pybind@0.1.0:', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-rtree@0.8.3:', type=('build', 'run'))
    depends_on('py-scikit-image@0.17.2:', type=('build', 'run'))
    depends_on('py-scipy@1.6.0:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-trimesh@2.38.10:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/app/test_flatmap.py")
