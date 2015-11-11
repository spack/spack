from spack import *

class Eigen(Package):
    """Eigen is a C++ template library for linear algebra: matrices, vectors,
    numerical solvers, and related algorithms.."""
    homepage = "http://eigen.tuxfamily.org/"
    url      = "http://bitbucket.org/eigen/eigen/get/3.2.5.tar.gz"

    version('3.2.5', '8cc513ac6ec687117acadddfcacf551b')

    def install(self, spec, prefix):
        import os 
        os.system("mkdir ./build_dir && cd ./build_dir")
        cmake('../', *std_cmake_args)

        make()
        make("install")
