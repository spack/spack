from spack import *

class Hypre(Package):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computation.llnl.gov/project/linear_solvers/software.php"
    url      = "http://computation.llnl.gov/project/linear_solvers/download/hypre-2.10.0b.tar.gz"

    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    def install(self, spec, prefix):
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(
                "--prefix=%s" % prefix,
                "--with-blas-libs=blas",
                "--with-blas-lib-dirs=%s/lib" % blas_dir,
                "--with-lapack-libs=\"lapack blas\"",
                "--with-lapack-lib-dirs=%s/lib" % lapack_dir,
                "--with-MPI")
            make()
            make("install")
