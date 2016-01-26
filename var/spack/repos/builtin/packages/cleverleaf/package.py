from spack import *

class Cleverleaf(Package):
    """
    CleverLeaf is a hydrodynamics mini-app that extends CloverLeaf with Adaptive
    Mesh Refinement using the SAMRAI toolkit from Lawrence Livermore National
    Laboratory. The primary goal of CleverLeaf is to evaluate the application of
    AMR to the Lagrangian-Eulerian hydrodynamics scheme used by CloverLeaf.
    """

    homepage = "http://uk-mac.github.io/CleverLeaf/"
    url      = "https://github.com/UK-MAC/CleverLeaf/tarball/master"

    version('develop', git='https://github.com/UK-MAC/CleverLeaf_ref.git', branch='develop')

    depends_on("SAMRAI@3.8.0:")
    depends_on("hdf5+mpi")
    depends_on("boost")

    def install(self, spec, prefix):
        cmake(*std_cmake_args)
        make()
        make("install")
