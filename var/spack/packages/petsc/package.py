from spack import *

class Petsc(Package):
    """PETSc is a suite of data structures and routines for the
       scalable (parallel) solution of scientific applications modeled by
       partial differential equations."""

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url      = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz"

    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f')
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13')
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f')

    depends_on("boost")
    depends_on("blas")
    depends_on("lapack")
    depends_on("hypre")
    depends_on("parmetis")
    depends_on("metis")
    depends_on("hdf5")
    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "CC=cc",
                  "CXX=c++",
                  "FC=f90",
                  "--with-blas-lib=%s/libblas.a"     % spec['blas'].prefix.lib,
                  "--with-lapack-lib=%s/liblapack.a" % spec['lapack'].prefix.lib,
                  "--with-boost-dir=%s"              % spec['boost'].prefix,
                  "--with-hypre-dir=%s"              % spec['hypre'].prefix,
                  "--with-parmetis-dir=%s"           % spec['parmetis'].prefix,
                  "--with-metis-dir=%s"              % spec['metis'].prefix,
                  "--with-hdf5-dir=%s"               % spec['hdf5'].prefix,
                  "--with-shared-libraries=0")

        # PETSc has its own way of doing parallel make.
        make('MAKE_NP=%s' % make_jobs, parallel=False)
        make("install")
