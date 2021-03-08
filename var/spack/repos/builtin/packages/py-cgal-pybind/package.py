from spack import *


class PyCgalPybind(PythonPackage):
    """Internal Python bindgins for CGAL"""

    homepage = "example.com"
    git      = "ssh://bbpcode.epfl.ch/common/cgal-pybind"

    version('develop', submodules=True)

    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('cgal')
    depends_on('eigen')
    depends_on('py-pybind11')
    depends_on('py-numpy@1.12:', type=('build', 'run'))

