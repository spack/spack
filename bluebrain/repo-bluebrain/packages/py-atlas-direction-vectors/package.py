# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasDirectionVectors(PythonPackage):
    """Commands to compute direction vectors in volumetric brain regions."""
    homepage = "https://github.com/BlueBrain/atlas-direction-vectors"
    git      = "https://github.com/BlueBrain/atlas-direction-vectors.git"
    pypi     = "atlas-direction-vectors/atlas-direction-vectors-0.1.2.tar.gz"

    version('develop', branch='main')
    version('0.1.2', tag='d87ff0caa7e03f62fa03fcd3230c398c3f74f5b7f550ac204098befbba6b8f45')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-atlas-commons@0.1.4:', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-numpy-quaternion', type=('build', 'run'))
    depends_on('py-scipy@1.4.1:', type=('build', 'run'))
    depends_on('py-voxcell@3.0.0:', type=('build', 'run'))
    # note: this is an extra not declared in setup.py
    # since we're not opensourcing regiodesics
    # FIXME regiodesics requires an ancient boost
    # depends_on('regiodesics@0.1.0:', type='run')
    depends_on('py-pytest', type='test')

    def patch(self):
        # Purge version constraints caused by old (outdated) numba incompatibilities
        filter_file(r'\[numba\]', '', 'setup.py')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/app/test_direction_vectors.py")
