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

    #def patch(self):
    #    """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
    #    """
    #    if self.spec.satisfies('@gap-junctions'):
    #        return
    #    filter_file(r'(include_directories\()SYSTEM ',
    #                r'\1',
    #                'functionalizer/CMakeLists.txt')

    #def cmake_args(self):
    #    args = [
    #        '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
    #        '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)
    #    ]
    #    return args
