from spack import *

class Metis(Package):
    """METIS is a set of serial programs for partitioning graphs,
       partitioning finite element meshes, and producing fill reducing
       orderings for sparse matrices. The algorithms implemented in
       METIS are based on the multilevel recursive-bisection,
       multilevel k-way, and multi-constraint partitioning schemes
       developed in our lab."""

    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    url      = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def patch(self):
        filter_file(r'#define IDXTYPEWIDTH 32', '#define IDXTYPEWIDTH 64', 'include/metis.h',
                    string=True)


    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DGKLIB_PATH=../GKlib',
                  '-DBUILD_SHARED_LIBS=TRUE',
                  *std_cmake_args)
            make()
            make("install")

