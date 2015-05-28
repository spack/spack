from spack import *

class Petsc(Package):
    """PETSc is a suite of data structures and routines for the scalable (parallel) solution of scientific applications modeled by partial differential equations."""

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url      = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz"

    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f')
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13')
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f')

    depends_on("blas")
    depends_on("lapack")
    depends_on("hypre")
    depends_on("parmetis")
    depends_on("metis")
    depends_on("hdf5")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-blas-lib=%s/lib/libblas.a" % spec['blas'].prefix,
                  "--with-lapack-lib=%s/lib/liblapack.a" % spec['lapack'].prefix,
                  "--with-hypre-lib=%s/lib/libhypre.a" % spec['hypre'].prefix,
                  "--with-hypre-include=%s/include" % spec['hypre'].prefix,
                  "--with-parmetis-lib=%s/lib/libparmetis.a" % spec['parmetis'].prefix,
                  "--with-parmetis-include=%s/include" % spec['parmetis'].prefix,
                  "--with-metis-lib=%s/lib/libmetis.a" % spec['metis'].prefix,
                  "--with-metis-include=%s/include" % spec['metis'].prefix,
                  "--with-hdf5-lib=%s/lib/libhdf5.a" % spec['hdf5'].prefix,
                  "--with-hdf5-include=%s/include" % spec['hdf5'].prefix,
                  "--with-shared-libraries=0")

        make()
        make("install")
