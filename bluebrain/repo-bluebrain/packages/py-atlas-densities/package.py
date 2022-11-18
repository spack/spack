# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasDensities(PythonPackage):
    """Tools to compute volumetric cell densities in the rodent brain"""
    homepage = "https://github.com/BlueBrain/atlas-densities"
    git = "https://github.com/BlueBrain/atlas-densities.git"
    pypi = "atlas-densities/atlas-densities-0.1.2.tar.gz"

    version('develop', branch='main')
    version('0.1.3', sha256='4829cba3f6f2b80f0bccfa21808062d5ff8a5387916c752a528388d05095527e')

    depends_on('py-cgal-pybind@0.1.4:', type=('build', 'run'))
    depends_on('py-atlas-commons@0.1.4:', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-openpyxl@3.0.3:', type=('build', 'run'))
    depends_on('py-pandas@1.0.3:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-scipy@1.6.0:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-tqdm@4.44.1:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))

    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/app/test_cell_densities.py")
        python("-m", "pytest", "tests/app/test_combination.py")
        python("-m", "pytest", "tests/app/test_mtype_densities.py")
        python("-m", "pytest",
               "tests/app/test_refined_inhibitory_neuron_densities.py")
