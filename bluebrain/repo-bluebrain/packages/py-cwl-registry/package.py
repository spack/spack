# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCwlRegistry(PythonPackage):
    """Workflows registered in CWL format
    """
    homepage = "https://bbpgitlab.epfl.ch/nse/cwl-registry"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/cwl-registry.git"

    version('develop', branch='main')
    version('0.3.2', tag='cwl-registry-v0.3.2')

    depends_on('python@3.9:', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on("py-click@8.0.0:", type=('build', 'run'))
    depends_on('py-voxcell', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-libsonata', type=('build', 'run'))
    depends_on('py-nexusforge', type=('build', 'run'))
    depends_on('py-bba-data-push@1.0.4:', type=('build', 'run'))
    depends_on('py-joblib', type=('build', 'run'))
    depends_on('py-cwl-luigi@0.3.1:', type=('build', 'run'))
    depends_on('py-entity-management@1.2.0:', type=('build', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
