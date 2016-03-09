from spack import *
import os

class Hypre(Package):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computation.llnl.gov/project/linear_solvers/software.php"
    url      = "http://computation.llnl.gov/project/linear_solvers/download/hypre-2.10.0b.tar.gz"

    version('2.10.1', 'dc048c4cabb3cd549af72591474ad674')
    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')

    variant('shared', default=True, description="Build shared library version (disables static library)")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    def install(self, spec, prefix):
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix
        mpi_dir = spec['mpi'].prefix

        os.environ['CC'] = os.path.join(mpi_dir, 'bin', 'mpicc')
        os.environ['CXX'] = os.path.join(mpi_dir, 'bin', 'mpicxx')
        os.environ['F77'] = os.path.join(mpi_dir, 'bin', 'mpif77')


        configure_args = [
                "--prefix=%s" % prefix,
                "--with-lapack-libs=lapack",
                "--with-lapack-lib-dirs=%s/lib" % lapack_dir,
                "--with-blas-libs=blas",
                "--with-blas-lib-dirs=%s/lib" % blas_dir]
        if '+shared' in self.spec:
            configure_args.append("--enable-shared")

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(*configure_args)

            make()
            make("install")
