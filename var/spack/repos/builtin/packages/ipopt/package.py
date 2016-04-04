from spack import *

class Ipopt(Package):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://projects.coin-or.org/Ipopt"
    url      = "http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.4.tgz"

    version('3.12.4', '12a8ecaff8dd90025ddea6c65b49cb03')
    version('3.12.3', 'c560cbfa9cbf62acf8b485823c255a1b')
    version('3.12.2', 'ec1e855257d7de09e122c446506fb00d')
    version('3.12.1', 'ceaf895ce80c77778f2cab68ba9f17f3')
    version('3.12.0', 'f7dfc3aa106a6711a85214de7595e827')

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkg-config")
    depends_on("mumps+double~mpi") 
    
    def install(self, spec, prefix):
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix
        mumps_dir = spec['mumps'].prefix

        # Add directory with fake MPI headers in sequential MUMPS
        # install to header search path
        mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
        mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags

        # By convention, spack links blas & lapack libs to libblas & liblapack
        blas_lib = "-L%s" % blas_dir.lib + " -lblas"
        lapack_lib = "-L%s" % lapack_dir.lib + " -llapack"
        
        configure_args = [
            "--prefix=%s" % prefix,
            "--with-mumps-incdir=%s" % mumps_dir.include,
            "--with-mumps-lib=%s" % mumps_libcmd,
            "--enable-shared",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
            ]
        
        configure(*configure_args)

        # IPOPT does not build correctly in parallel on OS X
        make(parallel=False)
        make("test", parallel=False)
        make("install", parallel=False)
