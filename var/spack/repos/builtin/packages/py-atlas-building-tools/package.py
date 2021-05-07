# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlasBuildingTools(PythonPackage):
    """Python tools to build brain region atlases."""
    homepage = "https://bbpcode.epfl.ch/browse/code/nse/atlas-building-tools/tree/"
    git      = "ssh://bbpcode.epfl.ch/nse/atlas-building-tools"

    version('0.1.0', commit='4d2ca679e34d08c76f96f15ccd3cdeccd2044696')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-cgal-pybind', type=('build', 'run'))
    depends_on('py-click@3.0:', type=('build', 'run'))
    depends_on('py-networkx@2.5:', type=('build', 'run'))
    depends_on('py-nptyping@1.0.1', type=('build', 'run'))
    depends_on('py-numba@0.48.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    # numpy-quaternion version is capped because of an issue similar to
    # https://stackoverflow.com/questions/20518632/importerror-numpy-core-multiarray-failed-to-import
    depends_on('py-numpy-quaternion@2017.10.14.11.11.56:2019.12.11.22.25.52', type=('build', 'run'))
    depends_on('py-openpyxl@3.0.5:', type=('build', 'run'))
    depends_on('py-pandas@1.0.3:', type=('build', 'run'))
    depends_on('py-pillow@1.7.2:', type=('build', 'run'))
    depends_on('py-poisson-recon-pybind', type=('build', 'run'))
    depends_on('py-pynrrd@0.4.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-rtree@0.9.4:', type=('build', 'run'))
    depends_on('py-scipy@1.4.1:', type=('build', 'run'))
    depends_on('py-scikit-image@0.17.2:', type=('build', 'run'))
    depends_on('py-tqdm@4.44.1:', type=('build', 'run'))
    depends_on('py-trimesh@3.6.18:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0', type=('run', 'build'))
    depends_on('py-xlrd@1.0.0:', type=('build', 'run'))
    depends_on('regiodesics@0.1.0:', type='run')
    depends_on('ultraliser@0.2.0', type='run')
