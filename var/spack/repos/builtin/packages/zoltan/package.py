from spack import *

class Zoltan(Package):
    """The Zoltan library is a toolkit of parallel combinatorial algorithms for
       parallel, unstructured, and/or adaptive scientific applications.  Zoltan's
       largest component is a suite of dynamic load-balancing and paritioning
       algorithms that increase applications' parallel performance by reducing
       idle time.  Zoltan also has graph coloring and graph ordering algorithms,
       which are useful in task schedulers and parallel preconditioners."""

    homepage = "http://www.cs.sandia.gov/zoltan"
    base_url = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions"

    version('3.83', '1ff1bc93f91e12f2c533ddb01f2c095f')
    version('3.3', '5eb8f00bda634b25ceefa0122bd18d65')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('mpi', default=False, description='Enable MPI support')

    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        config_args = [
            '--enable-f90interface' if '+fortan' in spec else '--disable-f90interface',
            '--enable-mpi' if '+mpi' in spec else '--disable-mpi',
        ]

        if '+mpi' in spec:
            config_args.append('--with-mpi=%s' % spec['mpi'].prefix)
            config_args.append('--with-mpi-compilers=%s' % spec['mpi'].prefix.bin)

        # NOTE: Early versions of Zoltan come packaged with a few embedded
        # library packages (e.g. ParMETIS, Scotch), which messes with Spack's
        # ability to descend directly into the package's source directory.
        if spec.satisfies('@:3.3'):
            cd('Zoltan_v%s' % self.version)

        mkdirp('build')
        cd('build')

        config_zoltan = Executable('../configure')
        config_zoltan('--prefix=%s' % pwd(), *config_args)

        make()
        make('install')

        mkdirp(prefix)
        move('include', prefix)
        move('lib', prefix)

    def url_for_version(self, version):
        return '%s/zoltan_distrib_v%s.tar.gz' % (Zoltan.base_url, version)
