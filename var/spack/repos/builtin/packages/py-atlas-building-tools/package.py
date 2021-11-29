# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlasBuildingTools(PythonPackage):
    """BBP Python tools to build brain region atlases."""
    homepage = "https://bbpgitlab.epfl.ch/nse/atlas-building-tools"
    git      = "git@bbpgitlab.epfl.ch:nse/atlas-building-tools.git"

    version('0.1.7', tag='atlas-building-tools-v0.1.7')
    version('0.1.6', tag='atlas-building-tools-v0.1.6')
    version('0.1.5', tag='atlas-building-tools-v0.1.5')
    version('0.1.4', tag='atlas-building-tools-v0.1.4')
    version('0.1.3', tag='atlas-building-tools-v0.1.3')
    version('0.1.2', tag='atlas-building-tools-v0.1.2')
    version('0.1.1', tag='atlas_building_tools-v0.1.1')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-cgal-pybind@0.1.1:', type=('build', 'run'), when='@0.1.2:')
    depends_on('py-cgal-pybind@0.1.0:', type=('build', 'run'), when='@0.1.1')
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-networkx@2.4:', type=('build', 'run'))
    depends_on('py-nptyping@1.0.1:', type=('build', 'run'))
    depends_on('py-numba', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    # numpy-quaternion version is capped because of an issue similar to
    # https://stackoverflow.com/questions/20518632/importerror-numpy-core-multiarray-failed-to-import
    depends_on('py-numpy-quaternion', type=('build', 'run'))
    depends_on('py-openpyxl@3.0.3:', type=('build', 'run'))
    depends_on('py-pandas@1.0.3:', type=('build', 'run'))
    depends_on('py-pillow@7.1.2:', type=('build', 'run'))
    depends_on('py-poisson-recon-pybind@0.1.0:', type=('build', 'run'))
    depends_on('py-pynrrd@0.4.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-rtree@0.8.3:', type=('build', 'run'))
    depends_on('py-scipy@1.4.1:', type=('build', 'run'))
    depends_on('py-scikit-image@0.17.2:', type=('build', 'run'))
    depends_on('py-tqdm@4.44.1:', type=('build', 'run'))
    depends_on('py-trimesh@2.38.10:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))
    depends_on('py-xlrd@1.0.0:', type=('build', 'run'))
    depends_on('regiodesics@0.1.0:', type='run')
    depends_on('ultraliser@0.2.0:', type='run')
    depends_on('py-pytest', type='test')

    def patch(self):
        # Purge version constraints caused by old (outdated) numba incompatibilities
        filter_file(r'"numba.*",', '"numba",', 'setup.py')
        filter_file(r'"numpy-quaternion.*",', '"numpy-quaternion",', 'setup.py')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/app/test_flatmap.py")
